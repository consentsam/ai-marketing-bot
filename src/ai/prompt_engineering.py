"""
Prompt engineering for the YieldFi AI Agent.

This module provides functionality for constructing prompts for AI-generated responses.
"""

from typing import Dict, Any, List, Optional

from src.config.settings import get_config
from src.models.tweet import Tweet
from src.models.account import Account, AccountType
from src.models.response import ResponseType
from src.utils.logging import get_logger

# Logger instance
logger = get_logger('prompt_engineering')


def create_prompt(
    tweet: Optional[Tweet] = None,
    response_type: ResponseType = ResponseType.TWEET_REPLY,
    responding_as: Optional[str] = None,
    target_account: Optional[Account] = None,
    tone: Optional[str] = None,
    max_length: Optional[int] = None,
    yieldfi_context: Optional[Dict[str, Any]] = None,
    include_examples: bool = True
) -> str:
    """Create a prompt for generating AI responses.
    
    Args:
        tweet: Source tweet to respond to
        response_type: Type of response to generate
        responding_as: Account type responding (e.g., "official", "intern")
        target_account: Target account to respond to
        tone: Desired tone of the response
        max_length: Maximum length of the response in characters
        yieldfi_context: Additional context about YieldFi
        include_examples: Whether to include examples in the prompt
        
    Returns:
        Prompt string
    """
    # Determine the responding account type
    if responding_as is None:
        responding_as = "official"
    
    # Default max length if not provided
    if max_length is None:
        max_length = 280
    
    # Default YieldFi context if not provided
    if yieldfi_context is None:
        yieldfi_context = {}
    
    # Start building the prompt
    prompt_parts = []
    
    # Add the system context
    prompt_parts.append(_get_system_context(responding_as, yieldfi_context))
    
    # Add examples if requested
    if include_examples:
        examples = _get_examples(response_type, responding_as, target_account)
        if examples:
            prompt_parts.append("\nHere are some examples of similar responses:")
            prompt_parts.append(examples)
    
    # Add information about the tweet if provided
    if tweet is not None:
        prompt_parts.append(f"\nThe tweet to respond to: \"{tweet.content}\"")
        
        # Add tone information if available
        if tweet.tone is not None:
            prompt_parts.append(f"The tone of the tweet is {tweet.tone}.")
        
        # Add tweet metrics if available
        if (tweet.metadata.like_count is not None or
            tweet.metadata.retweet_count is not None or
            tweet.metadata.reply_count is not None):
            metrics = []
            if tweet.metadata.like_count is not None:
                metrics.append(f"{tweet.metadata.like_count} likes")
            if tweet.metadata.retweet_count is not None:
                metrics.append(f"{tweet.metadata.retweet_count} retweets")
            if tweet.metadata.reply_count is not None:
                metrics.append(f"{tweet.metadata.reply_count} replies")
            
            if metrics:
                prompt_parts.append(f"The tweet has {', '.join(metrics)}.")
    
    # Add information about the target account if provided
    if target_account is not None:
        account_info = []
        account_info.append(f"You are responding to @{target_account.username}")
        
        if target_account.account_type != AccountType.UNKNOWN:
            account_info.append(f"who is a {target_account.account_type.name.lower().replace('_', ' ')}")
        
        if target_account.verified:
            account_info.append("(verified)")
        
        if target_account.follower_count is not None and target_account.follower_count > 0:
            account_info.append(f"with {target_account.follower_count} followers")
        
        if target_account.bio:
            account_info.append(f"Their bio: \"{target_account.bio}\"")
        
        if target_account.is_following_yieldfi:
            account_info.append("They are following YieldFi")
        
        if target_account.followed_by_yieldfi:
            account_info.append("YieldFi is following them")
        
        prompt_parts.append(" ".join(account_info) + ".")
    
    # Add instructions for the response
    prompt_parts.append(_get_response_instructions(
        response_type,
        responding_as,
        tone,
        max_length
    ))
    
    # Combine all parts into a single prompt
    prompt = "\n\n".join(prompt_parts)
    
    logger.debug("Generated prompt: %s", prompt[:200] + "..." if len(prompt) > 200 else prompt)
    
    return prompt


def _get_system_context(responding_as: str, yieldfi_context: Dict[str, Any]) -> str:
    """Get the system context for the prompt.
    
    Args:
        responding_as: Account type responding (e.g., "official", "intern")
        yieldfi_context: Additional context about YieldFi
        
    Returns:
        System context string
    """
    # Base YieldFi description
    base_description = """
    You are YieldFi, a DeFi protocol that offers liquid yield index products aggregating returns across blue-chip DeFi protocols.
    YieldFi provides one-click access to the best yields in DeFi with institutional-grade security through multi-sig wallets.
    Key products include YUSD (stablecoin yield), YETH (Ethereum yield), and YBTC (Bitcoin yield).
    YieldFi emphasizes security, transparency, and ease of use, making sophisticated yield generation accessible to everyone.
    """
    
    # Add YUSD details if available
    yusd_details = yieldfi_context.get('yusd', {})
    if yusd_details:
        if 'apy' in yusd_details:
            base_description += f" YUSD is currently offering {yusd_details['apy']}% APY."
    
    # Add YETH details if available
    yeth_details = yieldfi_context.get('yeth', {})
    if yeth_details:
        if 'apy' in yeth_details:
            base_description += f" YETH is currently offering {yeth_details['apy']}% APY."
    
    # Get the account-specific context
    if responding_as.lower() == 'official':
        account_context = """
        You are responding as the official YieldFi account. Your tone should be professional, informative, and helpful.
        You represent the protocol and should provide accurate information about YieldFi's features and benefits.
        """
    elif responding_as.lower() == 'intern':
        account_context = """
        You are responding as the YieldFi intern account. Your tone should be casual, friendly, and enthusiastic.
        You can be more conversational and use emojis, but you should still be knowledgeable about YieldFi.
        """
    else:
        account_context = """
        You are responding on behalf of YieldFi. Your tone should be professional yet approachable.
        You aim to provide helpful information about YieldFi and engage with the community.
        """
    
    return base_description.strip() + "\n\n" + account_context.strip()


def _get_examples(
    response_type: ResponseType,
    responding_as: str,
    target_account: Optional[Account] = None
) -> str:
    """Get examples of similar responses.
    
    Args:
        response_type: Type of response to generate
        responding_as: Account type responding (e.g., "official", "intern")
        target_account: Target account to respond to
        
    Returns:
        Examples string
    """
    examples = []
    
    # Official account examples
    if responding_as.lower() == 'official':
        if response_type == ResponseType.TWEET_REPLY:
            examples.extend([
                "Tweet: \"What's the current APY for YUSD?\"\nResponse: \"YUSD is currently offering 8.2% APY, which is among the highest for stablecoin yield products in DeFi. You can mint YUSD directly on our platform at https://yield.fi 💸\"",
                "Tweet: \"How does YieldFi ensure security of funds?\"\nResponse: \"YieldFi uses multi-sig wallets with a 3/5 signing threshold for all managed assets. This institutional-grade security ensures your funds are protected while earning the best yields in DeFi. Learn more about our security model: https://docs.yield.fi/concepts/custody-solution\"",
                "Tweet: \"Is there a minimum amount required to use YieldFi?\"\nResponse: \"There's no minimum amount required to mint YieldFi tokens! You can start with any amount you're comfortable with. Our protocol is designed to be accessible to everyone, from small retail users to large institutions.\"",
            ])
        elif response_type == ResponseType.ANNOUNCEMENT:
            examples.extend([
                "We're excited to announce that YieldFi now supports cross-chain yield optimization! Deploy your assets on Ethereum, Arbitrum, Optimism, and more, all while earning the best yields in DeFi. Learn more: https://yield.fi/multi-chain 🌉",
                "Security update: YieldFi has successfully completed its third security audit with @HalbornSecurity. All vaults have been thoroughly reviewed and approved, ensuring your assets remain safe while earning top yields. Read the full audit report: https://docs.yield.fi/audits 🔒",
            ])
    
    # Intern account examples
    elif responding_as.lower() == 'intern':
        if response_type == ResponseType.TWEET_REPLY:
            examples.extend([
                "Tweet: \"What makes YieldFi different from other yield protocols?\"\nResponse: \"The secret sauce is our institutional approach to DeFi yields! 🧙‍♂️ We use multi-sig wallets (unlike others who keep funds in smart contracts) and focus ONLY on blue-chip protocols with $1B+ TVL. Plus our team has 50+ years of quant finance experience! 🚀\"",
                "Tweet: \"Just tried YieldFi for the first time!\"\nResponse: \"Woohoo! Welcome to the YieldFi fam! 🎉 How are you liking it so far? I've been using YUSD for my stablecoin yield and it's been absolutely crushing it! Let me know if you have any questions - always happy to help! 😊\"",
                "Tweet: \"When will YieldFi support Solana?\"\nResponse: \"👀 I see you're interested in Solana support! While I can't share exact dates yet, I can tell you our team is working on expanding to more chains! Solana is definitely on our radar. I'll pass your interest along to the team! Would be amazing to bring our yields to the Solana fam! 🌞\"",
            ])
        elif response_type == ResponseType.PRODUCT_UPDATE:
            examples.extend([
                "📊 Dashboard upgrade alert! 📊 Check out our new analytics page showing real-time yield comparisons across ALL major DeFi protocols! Now you can see exactly how YieldFi is outperforming others! The data doesn't lie! 📈 https://yield.fi/analytics",
                "🔥 YUSD just got an APY boost! 🔥 We've optimized our yield strategies and now YUSD is earning 9.2% APY - that's 2% higher than last week! Not staking your stables with us yet? You're literally leaving money on the table! 💸 https://yield.fi/mint",
            ])
    
    # If we have a target account, try to get account-specific examples
    if target_account is not None:
        if target_account.account_type == AccountType.PARTNER:
            if responding_as.lower() == 'official':
                examples.extend([
                    "Tweet: \"Excited to explore potential collaborations with @YieldFi_Official!\"\nResponse: \"We're equally excited about the potential collaboration, @PartnerProtocol! YieldFi's institutional-grade yield strategies could bring significant value to your users. Let's connect - our team will reach out via DM to discuss further. Looking forward to what we can build together!\"",
                ])
            elif responding_as.lower() == 'intern':
                examples.extend([
                    "Tweet: \"Looking forward to our upcoming integration with @YieldFi_Official!\"\nResponse: \"The feeling is mutual, @PartnerProtocol! 🤝 Can't wait to see our protocols working together to bring even more value to DeFi users! This collab is going to be EPIC! 🚀 The whole YieldFi team is buzzing with excitement! 🐝\"",
                ])
        elif target_account.account_type == AccountType.KOL:
            if responding_as.lower() == 'official':
                examples.extend([
                    "Tweet: \"Been testing @YieldFi_Official and I'm impressed with the yield optimization.\"\nResponse: \"Thank you for the kind words, @CryptoInfluencer! We're committed to providing the best risk-adjusted yields in DeFi. We'd love to hear more of your thoughts - perhaps on a Twitter Space? Feel free to DM us to discuss further.\"",
                ])
    
    return "\n\n".join(examples)


def _get_response_instructions(
    response_type: ResponseType,
    responding_as: str,
    tone: Optional[str] = None,
    max_length: Optional[int] = None
) -> str:
    """Get instructions for the AI response.
    
    Args:
        response_type: Type of response to generate
        responding_as: Account type responding (e.g., "official", "intern")
        tone: Desired tone of the response
        max_length: Maximum length of the response in characters
        
    Returns:
        Instructions string
    """
    # Start with common instructions
    instructions = f"Please generate a {responding_as} YieldFi {response_type.name.lower().replace('_', ' ')}."
    
    # Add tone instruction if provided
    if tone is not None:
        instructions += f" The tone should be {tone}."
    
    # Add length instruction
    if max_length is not None:
        instructions += f" Keep the response under {max_length} characters to fit within Twitter's limits."
    
    # Add response type specific instructions
    if response_type == ResponseType.TWEET_REPLY:
        instructions += """
        The reply should be helpful, informative, and directly address the tweet's content or question.
        Make sure the response feels personalized and not generic.
        If appropriate, include a call to action like visiting the website or learning more.
        """
    elif response_type == ResponseType.NEW_TWEET:
        instructions += """
        Create an engaging standalone tweet that highlights a feature, benefit, or update about YieldFi.
        The tweet should be interesting and informative, providing value to followers.
        Include relevant hashtags if appropriate, but don't overuse them.
        """
    elif response_type == ResponseType.ANNOUNCEMENT:
        instructions += """
        Create an official announcement about YieldFi.
        The announcement should be clear, professional, and highlight the importance of the news.
        Include specific details that would be valuable to users and the wider DeFi community.
        """
    elif response_type == ResponseType.PRODUCT_UPDATE:
        instructions += """
        Create an update about a YieldFi product improvement or new feature.
        Focus on the benefits to users and how it enhances their experience.
        Include specific details about the update, such as new yields, features, or improvements.
        """
    elif response_type == ResponseType.COMMUNITY_UPDATE:
        instructions += """
        Create an update focused on the YieldFi community.
        This could include milestones, community events, or expressions of gratitude.
        The tone should be communal and appreciative of the community's support.
        """
    elif response_type == ResponseType.EVENT:
        instructions += """
        Create content related to an event that YieldFi is participating in or hosting.
        Include key details like date, time, and how users can participate.
        Convey excitement and the value of attending or participating in the event.
        """
    
    # Add account-specific instructions
    if responding_as.lower() == 'official':
        instructions += """
        As the official account, maintain a professional tone while being approachable.
        Ensure all information is accurate and reflects the protocol's official stance.
        Avoid excessive emojis, slang, or overly casual language.
        """
    elif responding_as.lower() == 'intern':
        instructions += """
        As the intern account, you can be more casual, energetic, and use emojis.
        Show enthusiasm and personality, but still be knowledgeable about YieldFi.
        You can use conversational language, but avoid being unprofessional.
        """
    
    return instructions


def generate_reply_prompt(original_post_content: str,
                          active_account_type: AccountType,
                          target_account_type: AccountType,
                          yieldfi_knowledge_snippet: str,
                          interaction_goal: str,  # e.g., "inform", "engage", "clarify"
                          style_preferences: dict  # e.g., {"tone": "professional", "length": "concise"}
                         ) -> str:
    """Generate a dynamic reply prompt based on interaction context.
    
    Args:
        original_post_content: The content of the original post to respond to.
        active_account_type: The type of the account responding (e.g., Official, Intern).
        target_account_type: The type of the account being responded to (e.g., Partner, KOL).
        yieldfi_knowledge_snippet: Relevant information about YieldFi to include in the response.
        interaction_goal: The goal of the interaction (e.g., "inform", "engage", "clarify").
        style_preferences: Preferences for the style of the response (tone, length).
        
    Returns:
        A formatted prompt string for generating a reply.
    """
    base_prompt = f"You are a {active_account_type.value} representative for YieldFi. "\
                  f"You are interacting with a {target_account_type.value}. "\
                  f"The original message is: '{original_post_content}'.\n\n"

    knowledge_context = f"Relevant YieldFi Information: {yieldfi_knowledge_snippet}\n\n"

    instruction = ""
    if active_account_type == AccountType.OFFICIAL and target_account_type == AccountType.PARTNER:
        instruction = "Craft a professional and collaborative reply. Focus on mutual benefits and upcoming opportunities. "
    elif active_account_type == AccountType.INTERN and target_account_type == AccountType.INTERN:
        instruction = "Craft a friendly and engaging reply. Be slightly informal but maintain respect. Share insights if appropriate. "
    # Add more conditions based on other prompt examples and interaction types

    goal_instruction = f"Your goal for this interaction is to {interaction_goal}. "
    style_instruction = f"Adopt a {style_preferences.get('tone', 'neutral')} tone. Keep the reply {style_preferences.get('length', 'moderately detailed')}. "

    return f"{base_prompt}{knowledge_context}{instruction}{goal_instruction}{style_instruction}Suggest a suitable reply:" 