# Table of Contents

- [Introduction](#introduction)
- [Problem & Solution](#problem-solution)
- [How It Works](#how-it-works)
- [FAQs](#faqs)
- [USPs](#usps)
- [YToken Vaults](#ytoken-vaults)
- [Mint](#mint)
- [LP Program](#lp-program)
- [Transparency](#transparency)
- [V2 Contract Addresses](#v2-contract-addresses)
- [Architecture](#architecture)
- [Smart Contract Interaction](#smart-contract-interaction)
- [YUSD](#yusd)
- [YETH](#yeth)
- [YBTC](#ybtc)
- [YLP](#ylp)
- [Swap](#swap)
- [Custody Solution](#custody-solution)
- [Risk Management](#risk-management)
- [Reserve Fund](#reserve-fund)
- [Audits](#audits)
- [Oracles](#oracles)
- [Brand Kit](#brand-kit)
- [General Risk Disclosures](#general-risk-disclosures)
- [Privacy Policy](#privacy-policy)
- [Terms of Service](#terms-of-service)
- [Old Contract Addresses](#old-contract-addresses)

---


# Introduction

Source: https://docs.yield.fi

[NextProblem & Solution](/problem-and-solution)Last updated 2 months ago

---


# Problem & Solution

Source: https://docs.yield.fi/problem-and-solution

DeFi has experienced **exponential growth** since the last cycle, unlocking unprecedented yield opportunities. However, this rapid expansion has also introduced **significant complexity**, making it difficult for everyday investors to navigate. With **new yield primitives, multiple chains, and fragmented ecosystems**, capturing the best returns requires constant monitoring, deep expertise, and access to institutional-grade opportunities—**barriers that most users cannot overcome**.

## **Key Challenges in DeFi**

1. **Fragmented Opportunities** – Hundreds of chains, thousands of protocols, and ever-evolving markets make it **humanly impossible** to track and capture the best opportunities in real-time.
2. **Dynamic Yield** – Almost all protocols use **variable yield mechanisms** to balance supply and demand, forcing users to **constantly rebalance** and manage opportunity costs.
3. **Varying Market Depth** – Liquidity fluctuates between **$50M to $500M**, with crypto markets operating **24/7**, requiring users to **time entries and exits perfectly** to avoid slippage and inefficiencies.
4. **Private Deals & Institutional Advantages** – Retail users consistently receive **inferior returns**, while institutions secure **exclusive incentives, lower risks, and better downside protection**—creating an uneven playing field.
5. **Due Diligence Challenges** – Teams **constantly upgrade** smart contracts post-audit, making it **nearly impossible** for average users to track changes, conduct deep security assessments, do background checks and evaluate economic risks effectively.

## **YieldFi’s Solution**

YieldFi eliminates this complexity by offering **liquid yield index products** that aggregate and optimize returns across **blue-chip DeFi protocols**. 

With automated, institutional-grade strategies, retail users and foundations can **access the best yield across DeFi — without the hassle, risk, or information asymmetry**.

[PreviousIntroduction](/)[NextHow It Works](/how-it-works)Last updated 2 months ago

---


# How It Works

Source: https://docs.yield.fi/how-it-works

YieldFi simplifies access to DeFi’s best yield opportunities through a secure, automated, and **institutionally structured** process.

1. **Deposit & Tokenization** – Users deposit **whitelisted assets** into the vault and receive a **yield index token** (ERC-4626 on Ethereum, ERC-20 on other chains), representing their share of the vault.
2. **Secure Custody** – All assets are transferred to **whitelisted multi-sig wallets**, requiring a minimum of 3 out of 5 signers to approve any transaction, ensuring maximum security and transparency.
3. **Automated Yield Deployment** – Assets from multi-sig wallets are allocated into **whitelisted, blue-chip DeFi protocols** to acquire **yield-bearing assets**, following a predefined vault strategy.
4. **Daily Yield Distribution** – Returns from different yield-bearing assets are **pooled and settled daily** to the vault, where the **index token is priced mark-to-market** to reflect real-time yield accrual.
5. **Continuous Optimization** – The system is **monitored 24/7** to dynamically optimize returns while **minimizing risks**.

## **Security First: Eliminating Smart Contract Risk**

YieldFi holds **zero user assets** in its smart contracts (except for processing redemption requests). This virtually eliminates self smart contract risk.

[PreviousProblem & Solution](/problem-and-solution)[NextFAQs](/faqs)Last updated 1 month ago

---


# FAQs

Source: https://docs.yield.fi/faqs

[PreviousHow It Works](/how-it-works)[NextUSPs](/usps)Last updated 1 month ago

---


# USPs

Source: https://docs.yield.fi/usps

YieldFi bridges the institutional precision of BlackRock with the accessibility and innovation of DeFi, offering a seamless, secure, and transparent yield generation experience:

1. **One-Click Access** – Simplify yield generation with **effortless access** to the best opportunities across DeFi and CeFi, tailored for all investors.
2. **Multi-Chain Compatibility** – Supports all major Layer 1 (L1) and Layer 2 (L2) networks, ensuring no ecosystem is deprived of high-yield opportunities.
3. **100% Transparency** – Fully **verifiable proof of reserves and proof of yield**, empowering users with unparalleled visibility into asset performance and security.
4. **Unmatched Security** – Assets are stored on-chain in multi-sig wallets with a 3-out-of-5 signing threshold, eliminating off-chain risks and reinforcing institutional-grade safeguards.
5. **Triple-Audit Assurance** – Independently audited by Halborn, Spearbit / Cantina, and SmartState, guaranteeing the highest standards of code security and operational reliability.
6. **Blue-Chip Protocols Only** – Capital is exclusively deployed in top-tier protocols with over $1 billion in assets under management and a proven track record of more than one year, ensuring stability and trustworthiness.
7. **Proven Leadership** – Led by a fully doxed team with over 50+ years of combined expertise in DeFi, quantitative finance, and fund management, backed by Tier-1 institutional and angel investors.

YieldFi combines institutional-grade rigor with retail accessibility, making **sophisticated yield generation simple, secure, and scalable for everyone.**

[PreviousFAQs](/faqs)[NextYToken Vaults](/technical-docs/ytoken-vaults)Last updated 1 month ago

---


# YToken Vaults

Source: https://docs.yield.fi/technical-docs/ytoken-vaults

## Overview

YToken Vaults form the foundation of the YieldFi protocol, offering users tokenized exposure to sophisticated yield-generating strategies. Each YToken represents a proportional claim on the underlying assets plus accumulated yield, enabling users to earn returns while maintaining liquidity.

We've crafted two distinct implementations to serve different blockchain environments:

* **YToken (L1)** - Our flagship implementation designed for Ethereum Mainnet, featuring full ERC4626 compliance and our innovative yield vesting mechanism that helps protect users from yield volatility.
* **YTokenL2** - Our streamlined implementation tailored specifically for Layer 2 networks, utilizing oracle-based pricing to minimize gas costs while maintaining the core benefits of YTokens.

## Core Concepts

## YTokenL1

## 1. Yield Distribution and Vesting

YToken vaults use a yield distribution mechanism that balances immediate value accrual with price stability.

When our strategies generate yield, the profits aren't immediately reflected in the token price. Instead, we gradually incorporate these profits into the exchange rate over a vesting period (typically 24 hours). This creates a steady increase in token value rather than sudden jumps.

The vesting mechanism serves several important purposes:

* Prevents abrupt exchange rate changes that could be exploited
* Protects against yield sniping where users deposit right before and withdraw right after yield distribution
* Creates a more predictable experience for all users

## 2. Asset Valuation

The value of YTokens is calculated through:

* **Total Assets Tracking**: We continuously account for all assets under management
* **Vesting-Aware Calculations**: When determining the exchange rate, we consider both fully vested yield and the portion of recent yield still in the vesting period

This approach ensures that token values grow smoothly and predictably, while still accurately reflecting the true value of the underlying assets.

## 3. Yield Vesting Mechanism

When profit is distributed to the vault, it enters a vesting period where it's gradually incorporated into the asset valuation. 

The vesting calculation uses a simple formula:

Copy
```
Unvested Amount = (Remaining Vesting Time / Total Vesting Period) × Vesting Amount
```
For example, if 1,000 USDC in yield was distributed 12 hours ago with a 24-hour vesting period, only 500 USDC would be reflected in the current exchange rate. The remaining 500 USDC would gradually vest over the next 12 hours.

This mechanism serves multiple purposes:

* Prevents abrupt exchange rate changes
* Protects against yield sniping attacks
* Incentivizes long-term holding
* Creates a more predictable user experience

## 4. Example: Yield Distribution and Vesting

When yield is distributed to a YToken vault, it goes through a specific process that ensures fair and predictable value accrual. Let's walk through a real-world example:

Imagine our yUSD vault has $100M worth of assets deployed across various lending protocols. On Monday at 3pm, these strategies collectively generate $100k in profit.

The distribution process follows these steps:

2. The Yield contract calls the YToken's reward function, indicating that $100k in profit should be added to the vault
5. The YToken contract records this new yield and starts the vesting clock, setting the current time (Monday 3pm) as the starting point for the 24-hour vesting period
8. The yield begins to affect the exchange rate gradually. If we check the value right after distribution:

	* Unvested Amount = (24 hours / 24 hours) × 100k = $100k
	* None of the yield is reflected in the current exchange rate yet
11. Six hours later (Monday 9pm):

	* Unvested Amount = (18 hours / 24 hours) × 100k = $75k
	* Only $25k of the yield is reflected in the exchange rate
14. Twelve hours later (Tuesday 3am):

	* Unvested Amount = (12 hours / 24 hours) × 100k = $50k
	* Half of the yield ($50k) is now reflected in the exchange rate
17. By Tuesday 3pm (24 hours after distribution):

	* Unvested Amount = (0 hours / 24 hours) × $100k = 0 USDC
	* The full $100k USDC yield is now incorporated into the exchange rate

This gradual incorporation creates a smooth, predictable increase in token value that makes it impossible for users to time deposits right before yield distribution and withdrawals right after. Whether you hold through the entire vesting period or not, you'll receive a fair proportion of the yield based on your holding duration.

## YTokenL2

YTokenL2 is an oracle-based implementation optimized for layer 2 networks, where cross-chain compatibility are paramount.

## 1. Oracle-Based Exchange Rate

Unlike our L1 implementation, YTokenL2 doesn't directly track assets through internal accounting. This reflects a fundamental architectural difference: the actual assets backing YTokenL2 tokens exist on L1, not on the L2 network itself.

Here's how this works:

When users interact with YTokenL2 on an L2 network, our offchain mechanism keeps track of these relationships and ensures that the exchange rates accurately reflect the true value of the underlying assets.

The Manager contract plays a crucial role in this system, helping update and synchronize values between the L1 and L2 environments. These synchronization are handled by the role based executor that syncs the values on L1, therefore these changes are accounted on YToken on L1 and bypass the need to be reflected in the L2 token values without requiring expensive cross-chain messaging for each update on every L2 chain.

Copy
```
function exchangeRate() public view returns (uint256) {
 require(oracle != address(0), "Oracle not set");

 uint256 rate = IOracleAdapter(oracle).fetchExchangeRate(address(this));
 require(rate > 0, "Invalid rate");

 // Convert from 18 decimals to asset decimals
 uint8 assetDecimals = IERC20Metadata(asset()).decimals();
 if (assetDecimals < 18) {
 return rate / (10 \*\* (18 - assetDecimals));
 }
 return rate;
}
```
This design offers several advantages:

* Eliminates the need for complex on-chain accounting
* Enables unified exchange rates across multiple networks
* Eliminates the need to account for each chain individually as the L1 serves as the source of truth from where exchange rate is published via oracles.

## 2. Unique Asset Valuation in YTokenL2

## Traditional ERC4626 vs. YTokenL2 Approach

Traditional ERC4626 vaults determine asset-to-share conversions using a fundamental formula:

Copy
```
shares = (assets \* totalSupply) / totalAssets
```
This approach requires the contract to track the total assets under management and maintain accurate accounting as assets flow in and out.

Copy
```
function \_convertToShares(uint256 assets, Math.Rounding rounding) internal view virtual override returns (uint256) {
 return assets.mulDiv(Constants.PINT, exchangeRate(), rounding); // Constants.PINT = 1e18
}

function \_convertToAssets(uint256 shares, Math.Rounding rounding) internal view virtual override returns (uint256) {
 return shares.mulDiv(exchangeRate(), Constants.PINT, rounding);
}
```
By relying on this oracle-based approach, the preview functions (`previewDeposit`, `previewMint`, `previewWithdraw`, and `previewRedeem`) all use the exchange rate rather than asset/supply ratios to determine expected amounts. This design reduces gas costs and simplifies cross-chain yield synchronization, making it particularly well-suited for L2 environments.

For example, if the exchange rate is 1.05e6 for a USDC-based vault, it means each YToken is worth 1.05 USDC.

[PreviousUSPs](/usps)[NextYUSD](/technical-docs/ytoken-vaults/yusd)Last updated 9 days ago

---


# Mint

Source: https://docs.yield.fi/guides/mint

Follow these steps to mint or redeem the yield bearing index product with ease:

1. **Select Your Chain**: Choose the blockchain you want to transact on.
2. **Connect Your Wallet**: Link your preferred crypto wallet.
3. **Pick Your Asset**: Select the yield index product you wish to mint or redeem.
4. **Approve**: Grant transaction permissions.
5. **Review & Mint/Redeem**: Confirm the details to finalize and click "Mint" or "Redeem".

**On Redemption**: You’ll receive an NFT with an **8-day cooldown period**. Once the cooldown ends, simply click “Claim” to burn your NFT and receive your desired asset directly in your wallet.

[PreviousSmart Contract Interaction](/technical-docs/smart-contract-interaction)[NextSwap](/guides/swap)Last updated 2 months ago

---


# LP Program

Source: https://docs.yield.fi/rewards-program/lp-program

[PreviousSwap](/guides/swap)[NextTransparency](/concepts/transparency)Last updated 4 months ago

---


# Transparency

Source: https://docs.yield.fi/concepts/transparency

[PreviousLP Program](/rewards-program/lp-program)[NextCustody Solution](/concepts/custody-solution)Last updated 2 months ago

---


# V2 Contract Addresses

Source: https://docs.yield.fi/resources/v2-contract-addresses

[PreviousReserve Fund](/concepts/reserve-fund)[NextOld Contract Addresses](/resources/v2-contract-addresses/old-contract-addresses)Last updated 20 hours ago

---


# Architecture

Source: https://docs.yield.fi/technical-docs/architecture

[PreviousYLP](/technical-docs/ytoken-vaults/ylp)[NextSmart Contract Interaction](/technical-docs/smart-contract-interaction)Last updated 1 month ago

---


# Smart Contract Interaction

Source: https://docs.yield.fi/technical-docs/smart-contract-interaction

## Mint YToken using Primary Asset

1. Since our vault follows ERC 4626 stadard, YToken can be minted instantly using Primary Asset YToken directly by calling deposit function on Vault contract.

Copy
```
 function deposit(uint256 assets, address receiver) public virtual returns (uint256) {
 uint256 maxAssets = maxDeposit(receiver);
 if (assets > maxAssets) {
 revert ERC4626ExceededMaxDeposit(receiver, assets, maxAssets);
 }

 uint256 shares = previewDeposit(assets);
 \_deposit(\_msgSender(), receiver, assets, shares);

 return shares;
 }
```
## Redeem YToken to Primary Asset

1. Redeeming YTokens for the primary asset token, can be done by calling `redeem` function on the Vault contract.
2. The Vault contract then places a redeem request on the Manager contract on behalf of the user.
3. Redeem requests are processed in a queue by the Keeper bot after a cooldown period.

Copy
```
 function redeem(uint256 shares, address receiver, address owner) public virtual returns (uint256) {
 uint256 maxShares = maxRedeem(owner);
 if (shares > maxShares) {
 revert ERC4626ExceededMaxRedeem(owner, shares, maxShares);
 }

 uint256 assets = previewRedeem(shares);
 \_withdraw(\_msgSender(), receiver, owner, assets, shares);

 return assets;
 }

```
## Mint YToken using non-Primary Asset via Manager

2. Users who want to mint YTokens using non-primary assets can do so by calling the `deposit` function on the Manager contract (along with passing \_referralCode if they have any).
5. Upon deposit, the user receives a receipt NFT as confirmation of the order placement.
8. This request is then picked up by the Keeper bot, which sends a transaction on-chain to burn the receipt NFT and mint YTokens to the user's address.

Copy
```
 /\*\*
 \* @notice Deposit the asset to the vault
 \* @param \_yToken address of the yToken
 \* @param \_asset address of the asset
 \* @param \_amount amount of the asset
 \* @param \_receiver address of the receiver
 \* @param \_callback address of the callback
 \* @param \_callbackData data of the callback
 \* @param \_referralCode bytes32 referral code for on-chain tracking
 \* @dev This function is used to deposit the asset to the vault
 \*/
 function deposit(address \_yToken, address \_asset, uint256 \_amount, address \_receiver, address \_callback, bytes calldata \_callbackData, bytes32 \_referralCode) external notPaused nonReentrant {
 \_validate(msg.sender, \_receiver, \_yToken, \_asset, \_amount, true);
 IERC20(\_asset).safeTransferFrom(msg.sender, address(this), \_amount);

 // get absolute exchange rate
 uint256 exchangeRateInUnderlying = IYToken(\_yToken).exchangeRate();

 // For all deposit via Manager, we mint the receipt and follow 2 step process
 // callback and callbackData are only for future use and can only be enabled by upgrading the contract
 uint256 receiptId = IReceipt(receipt).mint(msg.sender, Order(true, msg.sender, \_asset, \_receiver, \_yToken, \_amount, block.timestamp, exchangeRateInUnderlying, address(0), "", \_referralCode));
 emit OrderRequest(msg.sender, \_yToken, \_asset, \_receiver, \_amount, true, exchangeRateInUnderlying, receiptId, \_referralCode);
 }
```
## Redeem YToken using non-Primary Asset via Manager

2. Users can also place a redeem request for YUSD through the Manager contract.
5. These requests are maintained in a queue until the cooldown period is complete.
8. Once the cooldown period ends, the Keeper bot processes the redeem request and transfers the underlying asset to the user.

Copy
```
 /\*\*
 \* @notice Redeem the asset from the vault
 \* @param \_yToken address of the yToken
 \* @param \_asset address of the asset
 \* @param \_shares amount of the shares
 \* @param \_receiver address of the receiver
 \* @param \_callback address of the callback
 \* @param \_callbackData data of the callback
 \* @dev This function is used to redeem the asset from the vault
 \*
 \* @dev Example:
 \* When redeeming 100e18 YToken with exchange rate 1 YToken = 1.1 USDC:
 \* 1. Calculate vaultAssetAmount = 110e6 USDC (using convertToAssets)
 \* 2. Update yToken's total assets accounting to reflect the withdrawn amount
 \* 3. Burn the yToken shares immediately to stop yield accrual
 \* 4. Create a receipt for the withdrawal that can be executed after the waiting period
 \*/
 function redeem(address caller, address \_yToken, address \_asset, uint256 \_shares, address \_receiver, address \_callback, bytes calldata \_callbackData) external notPaused nonReentrant {
 if (msg.sender == \_yToken) {
 \_validate(caller, \_receiver, \_yToken, \_asset, \_shares, false);
 } else {
 require(caller == msg.sender, "!caller");
 \_validate(msg.sender, \_receiver, \_yToken, \_asset, \_shares, false);
 }

 // Calculate the equivalent vault asset amount
 uint256 vaultAssetAmount = IERC4626(\_yToken).convertToAssets(\_shares);

 // update equivalent total assets
 IYToken(\_yToken).updateTotalAssets(vaultAssetAmount, false);

 // burn shares from caller
 IYToken(\_yToken).burnYToken(caller, \_shares);

 /\*\*
 \* Post burning token, check the remaining shares for caller is either 0 or >= minSharesInYToken
 \* This is to ensure future redeems are not blocked due to low shares
 \*/
 uint256 remainingShares = IERC20(\_yToken).balanceOf(caller);
 require(remainingShares == 0 || remainingShares >= minSharesInYToken[\_yToken], "0 < remainingShares < minShares");

 // get exchange rate in underlying
 uint256 exchangeRateInUnderlying = IYToken(\_yToken).exchangeRate();

 // callback and callbackData are only for future use and can only be enabled by upgrading the contract
 uint256 receiptId = IReceipt(receipt).mint(caller, Order(false, caller, \_asset, \_receiver, \_yToken, \_shares, block.timestamp, exchangeRateInUnderlying, address(0), "", ""));
 emit OrderRequest(caller, \_yToken, \_asset, \_receiver, \_shares, false, exchangeRateInUnderlying, receiptId, ""); 
 }

```
[PreviousArchitecture](/technical-docs/architecture)[NextMint](/guides/mint)Last updated 9 days ago

---


# YUSD

Source: https://docs.yield.fi/technical-docs/ytoken-vaults/yusd

[PreviousYToken Vaults](/technical-docs/ytoken-vaults)[NextYETH](/technical-docs/ytoken-vaults/yeth)Last updated 9 days ago

---


# YETH

Source: https://docs.yield.fi/technical-docs/ytoken-vaults/yeth

## **Introduction**

YETH is our premier yield-bearing Ethereum asset, designed to offer users passive income while retaining full exposure to ETH. It serves as an optimal solution for DeFi participants looking to maximize yield without actively managing their holdings.

YETH integrates the ERC4626 standard with a yield vesting mechanism, ensuring a steady and predictable accrual of earnings. The token remains fully backed by Ethereum-based assets while seamlessly incorporating yield, making it ideal for both immediate liquidity and long-term accumulation strategies.

## **Underlying Asset**

YETH’s core asset is WETH (Wrapped Ether), a tokenized version of ETH that ensures broad compatibility across DeFi applications. WETH maintains a direct 1:1 peg with ETH, providing deep liquidity and seamless interaction within Ethereum’s ecosystem. We selected WETH due to its universal adoption and foundational role in DeFi infrastructure.

## **Supported Assets**

In addition to WETH, YETH’s Manager contract supports deposits of various Ethereum-based yield-generating assets, including:

* **stETH (Lido Staked ETH):** A liquid staking derivative (LSD) that represents staked ETH with automatic staking reward compounding.
* **rETH (Rocket Pool ETH):** A decentralized staking solution offering a non-custodial alternative to Lido.
* **ETHx (Stader ETH):** A staking derivative aimed at enhancing decentralization and accessibility within Ethereum’s staking ecosystem.
* **Pendle PT Tokens:** Principal tokens that strip out the yield component from underlying ETH assets, enabling fixed-rate returns.

When depositing non-native assets, the process follows a two-step flow:

1. The user deposits a supported asset (e.g., stETH) via the Manager contract and receives a Receipt NFT as confirmation of their pending deposit.
2. An off-chain executor then processes the deposit by:

	* Calculating asset to WETH where necessary, based on prevailing exchange rates.
	* Updating the totalAssets in YTokenL1 to reflect the new balance.
	* Minting the corresponding amount of YETH tokens for the user.

## **Yield Strategies**

YETH utilizes a diversified yield-generation framework, emphasizing three core strategies:

* **Yield Trading Protocols - Pendle, Spectra, and Napier:**

	+ Participation in tokenized yield markets to optimize staking yield.
	+ Leveraging structured yield instruments for predictable returns.
* **Staking & Liquid Derivatives:**

	+ Engaging with Ethereum staking solutions such as Lido, Rocket Pool, and Frax ETH.
	+ Earning staking rewards while maintaining liquidity via LSD protocols.
* **Lending & Liquidity Markets:**

	+ Deploying assets into established lending platforms like Aave, Morpho, and Euler.
	+ Securing yield through overcollateralized lending and liquidity provision.
* **Delta-Neutral Yield Strategies:**

	+ **Funding Rate Arbitrage:** Capturing inefficiencies in perpetual futures markets.
	+ **Hedged Strategies:** Structuring offsetting positions to generate passive returns with minimized price exposure.

Yield allocations are dynamically managed to optimize risk-adjusted returns, with strict exposure thresholds to maintain diversification and stability.

[PreviousYUSD](/technical-docs/ytoken-vaults/yusd)[NextYBTC](/technical-docs/ytoken-vaults/ybtc)Last updated 1 month ago

---


# YBTC

Source: https://docs.yield.fi/technical-docs/ytoken-vaults/ybtc

## **Introduction**

YBTC is a yield-generating Bitcoin asset designed to help users earn passive returns while keeping full exposure to BTC. It provides an efficient way for Bitcoin holders to participate in DeFi without actively managing their positions.

Built on the ERC4626 standard, YBTC ensures a structured and predictable yield distribution. It remains fully backed by Bitcoin-based assets, making it well-suited for users seeking both liquidity and long-term appreciation.

## **Underlying Asset**

The core asset backing YBTC is WBTC (Wrapped Bitcoin), a tokenized version of BTC that facilitates seamless integration with Ethereum-based DeFi applications. WBTC is backed 1:1 by Bitcoin and offers deep liquidity across various financial platforms. We chose WBTC due to its established trust, widespread adoption, and strong market presence.

## **Supported Assets**

Alongside WBTC, YBTC’s Manager contract supports deposits of other Bitcoin-related assets, including:

* **sBTC (Lido Staked BTC):** A liquid staking derivative that allows BTC holders to earn rewards while retaining liquidity.
* **tBTC (Threshold BTC):** A decentralized and non-custodial wrapped Bitcoin solution ensuring greater security and accessibility.
* **Pendle PT Tokens:** Principal tokens that separate fixed-yield components from underlying BTC assets, enabling stable returns.

Deposits of non-native assets follow a structured process:

1. Users deposit a supported asset (e.g., tBTC) through the Manager contract and receive a Receipt NFT as proof of deposit.
2. An off-chain executor then facilitates conversion and finalization by:

	* Calculating the equivalent value in WBTC terms based on current exchange rates
	* Updating totalAssets within YTokenL1 to reflect the new balance.
	* Issuing the appropriate amount of YBTC to the user.

## **Yield Strategies**

YBTC employs a diversified approach to yield generation, focusing on three primary categories:

* **Yield Trading Protocols - Pendle, Spectra, Napier, etc.**
Deployment in tokenized yield markets specializing in BTC-based instruments with predictable returns.
* **Lending Platforms - Aave, Spark, Flux**
Participation in lending markets offering stable and competitive BTC yields, ensuring capital efficiency.
* **Delta-Neutral Strategies**

	+ **Funding Rate Arbitrage:** Capturing rate differentials between BTC spot and derivative markets.
	+ **Hedged Positions:** Utilizing offsetting trades to mitigate directional risk while earning passive yield.

The allocation of yield strategies is actively managed to ensure a balance between risk and return while maintaining diversification across different yield sources.

[PreviousYETH](/technical-docs/ytoken-vaults/yeth)[NextYLP](/technical-docs/ytoken-vaults/ylp)Last updated 1 month ago

---


# YLP

Source: https://docs.yield.fi/technical-docs/ytoken-vaults/ylp

## Coming Soon!

[PreviousYBTC](/technical-docs/ytoken-vaults/ybtc)[NextArchitecture](/technical-docs/architecture)Last updated 1 month ago

---


# Swap

Source: https://docs.yield.fi/guides/swap

Buying / Selling yield index products is quick and effortless:

1. **Select Your Chain**: Choose the blockchain you want to transact on.
2. **Connect Your Wallet**: Link your preferred wallet to the YieldFi platform.
3. **Select Your Asset**: Choose the asset you want to swap for yield index product.
4. **Approve the Transaction**: Grant permission for the swap.
5. **Review & Swap**: Confirm the amounts and complete the swap.

That’s it! Your yield bearing index product is in your wallet, earning high yield without you need to do anything else.

[PreviousMint](/guides/mint)[NextLP Program](/rewards-program/lp-program)Last updated 2 months ago

---


# Custody Solution

Source: https://docs.yield.fi/concepts/custody-solution

YieldFi leverages industry-leading custody solutions— **Gnosis Safe Multi-Sig Wallets** —to ensure the highest level of asset security:

1. **Multi-Sig Wallets**: All assets are stored in whitelisted multi-sig wallets, requiring a minimum of 3 out of 5 signers to approve any transaction, ensuring maximum security and transparency.
2. **Institutional Safeguards**: Assets are protected by battle-tested multi-sig wallets, trusted by foundations, treasuries and global institutions, safeguarding more than $100Bn.
3. **Risk Mitigation**: Funds are never left idle in the smart contracts, reducing exposure to smart contract related vulnerabilities.

With Gnosis multi-sig at the core, YieldFi ensures that your assets remain secure, accessible, and always under institutional-grade protection.

[PreviousTransparency](/concepts/transparency)[NextRisk Management](/concepts/risk-management)Last updated 1 month ago

---


# Risk Management

Source: https://docs.yield.fi/concepts/risk-management

At YieldFi, risk management is at the core of our operations, ensuring yield generation without compromising safety:

1. **Institutional-Grade Custody**: Assets are secured using **Multi-Sig Wallets** (Gnosis Safe), eliminating single party risks.
2. **No Smart Contract Risk**: YieldFi's smart contracts have been audited multiple times by Tier 1 institutional auditors such as Halborn, Spearbit / Cantina, SmartState etc. Additionally, funds are never left idle in the smart contracts, reducing exposure to smart contract related vulnerabilities.
3. **Diversified Deployment**: Assets are split across trusted **DeFi protocols** (Pendle, Ethena, RWA), ensuring no single point of failure.
4. **Delta-Neutral Strategies**: Market-neutral strategies eliminates directional risk, providing stable returns regardless of price movements.
5. **Continuous Monitoring & Audits**: Systems are rigorously monitored, stress-tested, and audited to optimize yield and mitigate risks.
[PreviousCustody Solution](/concepts/custody-solution)[NextReserve Fund](/concepts/reserve-fund)Last updated 2 months ago

---


# Reserve Fund

Source: https://docs.yield.fi/concepts/reserve-fund

YieldFi maintains a dedicated **Reserve Fund** to safeguard user assets and ensure stability:

1. **Risk Coverage**: Acts as a buffer to cover unexpected losses from extreme market events.
2. **Sustainable Protection**: Funded through protocol revenue, ensuring long-term resilience.
3. **User Confidence**: Provides an added layer of security, reinforcing trust in YieldFi’s operations.

The Reserve Fund reflects YieldFi’s commitment to protecting users while delivering sustainable, risk-managed yields.

[PreviousRisk Management](/concepts/risk-management)[NextV2 Contract Addresses](/resources/v2-contract-addresses)Last updated 4 months ago

---


# Audits

Source: https://docs.yield.fi/resources/audits

[PreviousOld Contract Addresses](/resources/v2-contract-addresses/old-contract-addresses)[NextOracles](/resources/oracles)Last updated 10 days ago

---


# Oracles

Source: https://docs.yield.fi/resources/oracles

[PreviousAudits](/resources/audits)[NextBrand Kit](/resources/brand-kit)Last updated 1 month ago

---


# Brand Kit

Source: https://docs.yield.fi/resources/brand-kit

[PreviousOracles](/resources/oracles)[NextGeneral Risk Disclosures](/resources/general-risk-disclosures)Last updated 2 months ago

---


# General Risk Disclosures

Source: https://docs.yield.fi/resources/general-risk-disclosures

**General Risk Disclosures**

Please consider information in this Risk Disclosure Statement (“Statement”) as a general overview of the risks associated with the services offered by YieldFi and its affiliates (the “Services”) made for your awareness only. We do not intend to provide investment or legal advice through this Statement and make no representation that the Services described herein are suitable for you or that information contained herein is reliable, accurate or complete. We do not guarantee or make any representations or assume any liability regarding financial results based on the use of the information in this Statement, and further do not advise to rely on such information in the process of making a fully informed decision whether or not to use the Services. The risks outlined in this Statement are not exhaustive and this Statement only outlines the general nature of certain risks associated with crypto assets, and does not discuss in detail all risks associated with holding or trading crypto assets. Users should undertake their own assessment as to the suitability of using crypto assets and associated Services based on their own investigations, research and based on their experience, financial resources, and goals. You should not deal with crypto assets unless you understand their nature and the extent of your exposure to risk.

Note that specific disclosures and terms of service will apply with respect to various offerings of YieldFi, which will be published separately. Users should refer to those terms in addition to the disclosures herein when deciding whether to utilize the Services.

For the purpose of this Statement “you”, “your”, and “User” mean a user of our services and “we”, “us”, “our”, or “YieldFi”, mean YieldFi. Users are strongly advised to read this Risk Disclosure Statement carefully before deciding to start using the Services.

RISK OF LOSS IN TRADING CRYPTO ASSETS CAN BE SUBSTANTIAL AND YOU SHOULD, THEREFORE, CAREFULLY CONSIDER WHETHER SUCH ACTIVITY IS APPROPRIATE FOR YOU IN LIGHT OF YOUR CIRCUMSTANCES AND FINANCIAL RESOURCES. YOU SHOULD BE AWARE OF THE FOLLOWING:

**Crypto Assets Are Not Legal Tender In Most Jurisdictions**

Most crypto assets are not backed by any central government or legal tender (except in few, discrete cases), meaning each country has different standards. There is no assurance that a person who accepts crypto assets as payment today will continue to do so in the future. Holders of crypto assets put their trust in a digital, decentralized, and partially anonymous system that relies on peer-to-peer networks and cryptography to maintain its integrity, and neither vendors nor individuals have an obligation to accept crypto assets as payment in the future;

**Loss of value, Volatility and Uncertainty of Future Performance**

There is typically limited or no fundamental reasoning behind the pricing of crypto assets, creating the risk of volatility and unpredictability in the price of crypto assets relative to fiat currencies. Crypto assets have had historically higher price volatility than fiat currencies, including irrational and extreme moves in price as the process for valuation can be speculative and uncertain.

**Liquidity Risk**

Crypto assets can have limited liquidity that can make it difficult or impossible to sell or exit a position when desired. This can occur at any time, especially during periods of high volatility.

**Market forces**

Trading in crypto assets may be susceptible to irrational market forces, such as speculative bubbles, manipulation, scams, and fraud.

**Financial Crime and Cyber Attacks**

Cyber crime relating to crypto assets can be more prevalent than other financial crime as the ecosystem is totally digital and traditional governance and risk mitigants may be lacking. For example, a 51% attack is an attack on a blockchain by any person or group of persons who control more than 50% of the network. Attackers with majority control of a network can interrupt the recording of new blocks, alter payment history, and subvert funds. Users are susceptible to malware and fake/hijacked addresses and other forms of cyber-attacks and Users should always take care of passwords and double check the addresses and URLs before loading software or interacting with any platform, protocol, or service.

**Absence of Control**

YieldFi is not a broker, agent or advisor and has no fiduciary relationship or obligation to Users in connection with any transaction or other decision or activity undertaken by you using the Services. We do not control whether your use of the Services is consistent with your financial goals. It is up to Users to assess whether their financial resources are appropriate for their respective activity with us and risk appetite in the products and services you use.

**Availability of Services**

We do not guarantee that the Services will be available at any given time or that the Services will not be subject to unplanned service interruptions or network congestion. You may not be able to buy, sell, store, transfer, redeem, send, or receive crypto assets when you want to.

**Technology Risk**

The risks of crypto assets being transacted via new technologies (including distributed ledger technologies) include, among other things, anonymity, irreversibility of transactions, accidental transactions, transaction recording, and settlement. Transactions in crypto assets on a blockchain relies on the proper functioning of complex software, which exacerbates the risk of access to or use of crypto assets being impaired or prevented. Moreover, there is risk of failures, defects, hacks, exploits, protocol errors, or unforeseen circumstances that might occur in connection with a crypto asset or the technologies on which the crypto asset is based.

**Irreversible Transactions**

Transactions in crypto assets are generally irreversible. As a result, losses due to fraudulent or accidental transactions may not be recoverable.

**Third Party Risk**

Third parties such as payment providers, custodians, exchanges, and banking partners may be involved in the provision of the Services. You may be subject to the terms and conditions of these third parties, and YieldFi cannot be responsible for any losses these third parties may cause you.

**Taxation and Disclosure of Information**

You are responsible for determining the taxes to which you may be subject and their application when using the Services. It is your responsibility to report and pay any taxes that may arise from transactions and you acknowledge that YieldFi does not provide legal or tax advice regarding such transactions. If you have concerns about your tax treatment or obligations you may wish to seek independent advice.

You understand that when, where, and as required by applicable law, YieldFi will disclose available information relating to transactions transfers, distributions or payments to the appropriate regulatory and tax authorities or other public authorities. Similarly, when, where and as required by applicable law, YieldFi will withhold taxes related to your transactions, transfers, distributions or payments.

**No Investment and Legal Advice**

Communications or information provided by YieldFi shall not be considered or construed as investment advice, financial advice, trading advice, or any other type of advice. The User is the only party who can determine whether an investment, investment strategy or related transaction is appropriate based on his or her personal investment objectives, financial situation and risk tolerance, and shall be solely responsible for any losses or liabilities that may result.

**Regulatory Risk**

The regulation of crypto assets and platforms is uncertain in many jurisdictions and YieldFi cannot be held responsible for compliance with legal rules of countries from which customers, on their own initiative, access the Services. Moreover, changes in rules applicable to crypto assets may considerably impact on the prices of those assets and are unpredictable. You further acknowledge the above list of risks is non- exhaustive and there may also be unpredictable risks.

[PreviousBrand Kit](/resources/brand-kit)[NextPrivacy Policy](/resources/privacy-policy)Last updated 8 months ago

---


# Privacy Policy

Source: https://docs.yield.fi/resources/privacy-policy

This Privacy Policy for YieldFi ("Company", "we", "us" "our") describes how we collect, use and disclose information about users of the Company's website (yield.fi, the “Site”), and any related services, tools and features, including the YieldFi service (collectively, the "Services"). For the purposes of this Privacy Policy, "you" and "your" means you as the user of the Services. ​ Please read this Privacy Policy carefully. By using, accessing, or downloading any of the Services, you agree to the collection, use, and disclosure of your information as described in this Privacy Policy. If you do not agree to this Privacy Policy, please do not use, access or download any of the Services. ​

**UPDATING THIS PRIVACY POLICY** 

We may modify this Privacy Policy from time to time in which case we will update the "Last Revised" date at the top of this Privacy Policy. If we make material changes to how we use the information we collect, it is your responsibility to stay informed about these updates. You can check for notices of such changes on our website or review the Privacy Policy periodically. Continuing to use our Services after any changes indicates your acceptance of the updated Privacy Policy. If you do not agree with any updates, please do not access or continue to use the Services. ​

**COMPANY'S COLLECTION AND USE OF INFORMATION ​**

When you access or use the Services, we may collect (directly or through third-party providers) certain categories of information about you from a variety of sources, which comprises: ​

Information provided during “Know Your Customer” (“KYC”) and Anti-Money Laundering (“AML”) processes, which includes personal identifying information. This may include:

* Basic Information: Name, Address, Date of Birth, Nationality, Country of Residence, Phone Number, Email Address.
* Identification Information: Utility bills (or other proof of address), photographs, Government-issued identification (such as identification cards, passports, driver’s licenses, etc.), tax ID number, employment information, proof of residency, visa information, organizational documents, and information regarding ultimate beneficial owners.
* Financial Information: Income/net assets/wealth verification statements.

We process the data provided and collected to provide the Services, personalize your experience with the Services, and improve the Services. Specifically, we use your data to:

* identify you as a user in our system;
* provide you with our Service;
* improve the administration of our Service and quality of experience when you interact with our Service;
* provide customer support and respond to your requests and inquiries;
* investigate and address conduct that may violate our Terms of Use;
* detect, prevent, and address fraud, violations of our terms or policies, and/or other harmful or unlawful activity;
* send you administrative notifications, such as security, support, and maintenance advisories;
* send you newsletters, promotional materials, and other notices related to our Services or third parties' goods and services;
* respond to your inquiries related to employment opportunities or other requests;
* comply with applicable laws, cooperate with investigations by law enforcement or other authorities of suspected violations of law, and/or to pursue or defend against legal threats and/or claims; and
* act in any other way we may describe when you provide the Personal Data.

**HOW THE COMPANY SHARES YOUR INFORMATION** 

​In certain circumstances, the Company may share your information with third parties for legitimate purposes subject to this Privacy Policy. Such circumstances comprise of: ​

* Blockchain analysis service providers, including TRM​
* Data analytics vendors, including Google Analytics ​
* To comply with applicable law or any obligations thereunder, including cooperation with law enforcement, judicial orders, and regulatory inquiries ​
* In connection with an asset sale, merger, bankruptcy, or other business transaction ​
* To enforce any applicable terms of service ​
* To ensure the safety and security of the Company and/or its users ​
* With any parent companies, subsidiaries, joint ventures, or other companies under common control with us, in which case we will require such entities to honor this Privacy Policy
* In connection with or during negotiation of any merger, financing, acquisition, or dissolution transaction or proceeding involving sale, transfer, divestiture, or disclosure of all or a portion of our business or assets. In the event of an insolvency, bankruptcy, or receivership, data may also be transferred as a business asset. If another company acquires our company, business, or assets, that company will possess the data collected by us and will assume the rights and obligations regarding your data as described in this Privacy Policy.
* When you request us to share certain information with third parties, such as through your use of login integrations ​
* With professional advisors, such as auditors, law firms, or accounting firms ​

**COOKIES AND OTHER TRACKING TECHNOLOGIES** 

Do Not Track Signals ​ Your browser settings may allow you to transmit a "Do Not Track" signal when you visit various websites. Like many websites, our website is not designed to respond to "Do Not Track" signals received from browsers. To learn more about "Do Not Track" signals, you can visit http://www.allaboutdnt.com/. ​ Cookies and Other Tracking Technologies ​ Most browsers accept cookies automatically, but you may be able to control the way in which your devices permit the use of cookies, web beacons/clear gifs, other geolocation tracking technologies. If you so choose, you may block or delete our cookies from your browser; however, blocking or deleting cookies may cause some of the Services, including any portal features and general functionality, to work incorrectly. If you have questions regarding the specific information about you that we process or retain, as well as your choices regarding our collection and use practices, please contact us using the information listed below. ​ To opt out of tracking by Google Analytics, click here. ​ Your browser settings may allow you to transmit a "Do Not Track" signal when you visit various websites. Like many websites, our website is not designed to respond to "Do Not Track" signals received from browsers. To learn more about "Do Not Track" signals, you can visit http://www.allaboutdnt.com/. ​

**SOCIAL NETWORKS AND OTHER THIRD PARTY WEBSITES AND LINKS** 

We may provide links to websites or other online platforms operated by third parties, including third-party social networking platforms, such as Twitter, Discord, Telegram or Medium as well as Curve Finance & Uniswap, operated by third parties (such platforms are "Social Networks" or “Decentralized Finance Applications”). If you follow links to sites not affiliated or controlled by us, you should review their privacy and security policies and other terms and conditions. We do not guarantee and are not responsible for the privacy or security of these sites, including the accuracy, completeness, or reliability of information found on these sites. Information you provide on public or semi-public venues, including information you share or post on Social Networks, may also be accessible or viewable by other users of the Services and/or users of those third-party online platforms without limitation as to its use by us or by a third party. Our inclusion of such links does not, by itself, imply any endorsement of the content on such platforms or of their owners or operators, except as disclosed on the Services. ​

**THIRD PARTY WALLET EXTENSIONS** 

​Certain transactions conducted via our Services, will require you to connect a Wallet to the Services. By using such Wallet to conduct such transactions via the Services, you agree that your interactions with such third party Wallets are governed by the privacy policy for the applicable Wallet. We expressly disclaim any and all liability for actions arising from your use of third party Wallets, including but without limitation, to actions relating to the use and/or disclosure of personal information by such third party Wallets.

**PUBLIC INFORMATION OBSERVED FROM BLOCKCHAINS** 

We collect data from activity that is publicly visible and/or accessible on blockchains. This may include blockchain addresses and information regarding holdings, purchases, sales, or transfers of tokens, which may then be associated with other data you have provided to us.

**CHILDREN'S PRIVACY** 

Children under the age of 18 are not permitted to use the Services, and we do not seek or knowingly collect any personal information about children under 13 years of age. If we become aware that we have unknowingly collected information about a child under 13 years of age, we will make commercially reasonable efforts to delete such information from our database. ​ If you are the parent or guardian of a child under 13 years of age who has provided us with their personal information, you may contact us using the below information to request that it be deleted. ​

**DATA ACCESS AND CONTROL** 

You can view, access, edit, or delete your data for certain aspects of the Service via your Settings page. You may also have certain additional rights:

* If you are a user in the European Economic Area or United Kingdom, you have certain rights under the respective European and UK General Data Protection Regulations (“GDPR”). These include the right to (i) request access and obtain a copy of your personal data; (ii) request rectification or erasure; (iii) object to or restrict the processing of your personal data; and (iv) request portability of your personal data. Additionally, if we have collected and processed your personal data with your consent, you have the right to withdraw your consent at any time.
* If you are a California resident, you have certain rights under the California Consumer Privacy Act (“CCPA”). These include the right to (i) request access to, details regarding, and a copy of the personal information we have collected about you and/or shared with third parties; (ii) request deletion of the personal information that we have collected about you; and (iii) the right to opt-out of sale of your personal information. As the terms are defined under the CCPA, we do not “sell” your “personal information.”

If you wish to exercise your rights under the GDPR, CCPA, or other applicable data protection or privacy laws, please contact us at the address provided herein, specify your request, and reference the applicable law. We may ask you to verify your identity, or ask for more information about your request. We will consider and act upon any above request in accordance with applicable law. We will not discriminate against you for exercising any of these rights.

Notwithstanding the above, we cannot edit or delete any information that is stored on a blockchain, for example the Ethereum blockchain, as we do not have custody or control over any blockchains.

**DATA RETENTION** 

We may retain your data as long as you continue to use the Services, have an account with us, or for as long as is necessary to fulfill the purposes outlined in this Privacy Policy. We may continue to retain your data even after you deactivate your account and/or cease to use the Service if such retention is reasonably necessary to comply with our legal obligations, to resolve disputes, prevent fraud and abuse, enforce our Terms or other agreements, and/or protect our legitimate interests. Where your data is no longer required for these purposes, we will delete it.

**DATA SECURITY** 

Please be aware that, despite our reasonable efforts to protect your information, no security measures are perfect or impenetrable, and we cannot guarantee "perfect security." Please further note that any information you send to us electronically, while using the Services or otherwise interacting with us, may not be secure while in transit. We recommend that you do not use unsecure channels to communicate sensitive or confidential information to us. ​You are responsible for the security of your digital wallet(s), and urge you to take steps to ensure it is and remains secure.

In the event that any information under our custody and control is compromised as a result of a breach of security, we will take steps to investigate and remediate the situation and, in accordance with applicable laws and regulations, notify those individuals whose information may have been compromised.

**HOW TO CONTACT US** 

​Should you have any questions about our privacy practices or this Privacy Policy, please raise a ticket on our discord server.

[PreviousGeneral Risk Disclosures](/resources/general-risk-disclosures)[NextTerms of Service](/resources/terms-of-service)Last updated 8 months ago

---


# Terms of Service

Source: https://docs.yield.fi/resources/terms-of-service

[PreviousPrivacy Policy](/resources/privacy-policy)Last updated 8 months ago

---


# Old Contract Addresses

Source: https://docs.yield.fi/resources/v2-contract-addresses/old-contract-addresses

## Ethereum

ContractAddressManager 

yUSD

sUSD

Receipt

Bridge 

## Base

ContractAddressManager 

yUSD

sUSD

Receipt

Bridge 

## Arbitrum

ContractAddressyUSD

sUSD

Receipt

Bridge 

Manager 

## Optimism

ContractAddressyUSD

sUSD

Receipt

Bridge 

Manager 

## Tron

ContractAddressyUSD

sUSD

Receipt

Bridge 

TBD

Manager 

## TON

ContractAddressyUSD

TBD

sUSD

TBD

Receipt

TBD

Bridge 

TBD

Manager 

TBD

## Solana

ContractAddressyUSD

TBD

sUSD

TBD

Receipt

TBD

Bridge 

TBD

Manager 

TBD

## Polygon

ContractAddressyUSD

TBD

sUSD

TBD

Receipt

TBD

Bridge 

TBD

Manager 

TBD

## BSC

ContractAddressyUSD

TBD

sUSD

TBD

Receipt

TBD

Bridge 

TBD

Manager 

TBD

## Avalanche

ContractAddressyUSD

TBD

sUSD

TBD

Receipt

TBD

Bridge 

TBD

Manager 

TBD

## Arbitrum Sepolia (Testnet)

ContractAddressyUSD

sUSD

Receipt

Bridge 

Manager 

[PreviousV2 Contract Addresses](/resources/v2-contract-addresses)[NextAudits](/resources/audits)Last updated 2 months ago

---
