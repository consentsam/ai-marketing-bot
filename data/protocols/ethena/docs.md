# Table of Contents

- [Ethena Overview](#ethena-overview)
- [How USDe Works](#how-usde-works)
- [Genesis Story](#genesis-story)
- [How to Buy USDe](#how-to-buy-usde)
- [USDe Overview](#usde-overview)
- [Overview](#overview)
- [Custodian Attestations](#custodian-attestations)
- [How to [Un]lock positions](#how-to-un-lock-positions)
- [Underlying Derivatives](#underlying-derivatives)
- [Peg Arbitrage Mechanism](#peg-arbitrage-mechanism)
- [Scenario Analysis](#scenario-analysis)
- [Delta-Neutral Stability](#delta-neutral-stability)
- [Censorship Resistance](#censorship-resistance)
- [Inverse vs Linear Contracts](#inverse-vs-linear-contracts)
- [Basis Spread](#basis-spread)
- [Custodial Risk](#custodial-risk)
- [Exchange Failure Risk](#exchange-failure-risk)
- [Margin Collateral Risks](#margin-collateral-risks)
- [Risk Committee](#risk-committee)
- [Reserve Fund](#reserve-fund)
- [Key Addresses](#key-addresses)
- [Matrix of Multisig and Timelocks](#matrix-of-multisig-and-timelocks)
- [User Security Measures](#user-security-measures)
- [Mint & Redeem Key Functions](#mint-redeem-key-functions)
- [Internal Services](#internal-services)
- [Managing Risk from dependencies](#managing-risk-from-dependencies)
- [USDe + sUSDe Custodian Availability](#usde-susde-custodian-availability)
- [Audits](#audits)
- [General Risk Disclosures](#general-risk-disclosures)
- [Privacy Policy](#privacy-policy)
- [Terms of Service](#terms-of-service)
- [USDe Terms and Conditions - EEA](#usde-terms-and-conditions-eea)
- [USDe Terms and Conditions - Non EEA](#usde-terms-and-conditions-non-eea)
- [USDe Mint User Agreement - Non EEA](#usde-mint-user-agreement-non-eea)

---


# Ethena Overview

Source: https://docs.ethena.fi

Ethena's USDe is **not** the same as a fiat stablecoin like USDC or USDT. USDe is a synthetic dollar, backed with crypto assets and corresponding short futures positions.

This means that the risks implicated by interacting with USDe are inherently different. 

Please refer to our extensive [Risk](/solution-overview/risks)[s](/solution-overview/risks) section for more information.

## Overview

Ethena is a synthetic dollar protocol built on Ethereum that provides a crypto-native solution for money, *USDe*, alongside a globally accessible dollar savings asset, *sUSDe*.

Ethena's synthetic dollar, *USDe*, provides the crypto-native, scalable solution for money achieved by delta-hedging Bitcoin, Ethereum and Solana spot assets using perpetual and deliverable futures contracts, as well as holding liquid stables such as USDC and USDT. 

*USDe* is fully-backed (subject to the discussion in the Risks section regarding events potentially resulting in loss of backing) and free to compose throughout CeFi & DeFi.

*USDe* peg stability is supported through the use of delta hedging derivatives positions against protocol-held backing assets, maintaining a relatively stable value with reference to the value spot crypto assets as well as futures positions. 

The inclusion of liquid stables (such as USDC and USDT) enhances the efficiency of the delta hedging process, while also potentially acting as a safeguard in bear markets when funding rates and futures basis are suboptimal. Liquid stables may earn rewards depending on where they are held, potentially enhancing overall protocol revenue.

Website: <https://ethena.fi/>

Telegram: <https://t.me/ethena_labs>

Discord: [https://discord.gg/ethena](https://discord.gg/ethena ) 

Twitter: <https://twitter.com/ethena_labs>

LinkedIn: <https://www.linkedin.com/company/ethena-labs/>

## Quick Links

[How to Buy USDe](/video-guides/how-to-buy-usde)Users are currently able to:

* **Permissionless Acquire** *USDe.* Access external AMM pools to acquire or dispose of *USDe* with assets such as USDT or USDC.
* **Direct Mint** *USDe*. Transfer accepted reserve assets and receive *USDe, subject to clearing KYC/KYB checks exclusively for approved market making counterparties*. See Supplemental USDe Terms and Conditions.
* **Direct Redeem** *USDe*. Burn *USDe* & receive backing assets*, subject to clearing KYC/KYB checks exclusively for approved market making counterparties*. See Supplemental USDe Terms and Conditions.
* **Stake & Unstake** *USDe*. Receive rewards from protocol revenue. *Available exclusively for users in permitted jurisdictions.*

Last updated 3 months ago

Was this helpful?

---


# How USDe Works

Source: https://docs.ethena.fi/how-usde-works

Last updated 3 months ago

Was this helpful?

---


# Genesis Story

Source: https://docs.ethena.fi/genesis-story

In March 2023 Arthur Hayes published his piece ["Dust on Crust"](https://blog.bitmex.com/dust-on-crust/) which outlined his vision for the largest opportunity in crypto - creating a synthetic dollar using crypto collateral and derivatives.

The most important financial instrument on earth to save and preserve wealth is simply a dollar with a yield. It sounds simple, but the demand for this product is several orders of magnitude larger than the entire crypto market combined, including Bitcoin.

Ethena was built to provide this product and in doing so, force the convergence of capital and interest rates across DeFi, CeFi and TradFi via USDe.

Last updated 3 months ago

Was this helpful?

---


# How to Buy USDe

Source: https://docs.ethena.fi/video-guides/how-to-buy-usde

Last updated 5 months ago

Was this helpful?

---


# USDe Overview

Source: https://docs.ethena.fi/solution-overview/usde-overview

Ethena enables the creation and redemption of a delta-neutral synthetic dollar, *USDe*, crypto's first fully-backed, onchain, scalable, and censorship-resistant form of money. 

The mechanism backing *USDe* enables sUSDe, the first "Internet Money" offering a crypto-native, reward-accruing asset, derived from liquid asset rewards (to the extent utilized in backing) and the funding and basis spread available in perpetual and futures markets.

## Peg Stability Mechanism

*USDe* derives its relative peg stability from executing automated and programmatic delta-neutral hedges with respect to the underlying backing assets. 

Hedging the price change risk of the backing asset in the same size minimizes fluctuations in the backing asset price as the change in value of the backing assets asset is generally offset by the change in value of the hedge. 

This enables the synthetic USD value of the backing assets to remain relatively stable in most market conditions.

Ethena does not use any material leverage to margin the delta hedging derivatives positions beyond the natural state as a result of exchanges applying slight discounts to the value of backing assets to the extent used as backing and margin collateral on the initial hedge and issuance of *USDe*. 

## Key Information

1. Users are able to acquire USDe in permissionless external liquidity pools.
2. Approved parties from permitted jurisdictions who pass KYC/KYB screening are able to **mint** & **redeem** *USDe* on-demand with Ethena contracts directly following whitelisting. See Supplemental USDe Terms and Conditions.
3. There is minimal reliance upon traditional banking infrastructure as trustless backing assets are held and stored within the crypto ecosystem.

## **Mechanic Example**

1. A whitelisted user provides ~$100 of *USDT or USDC* and receives ~100 newly-minted *USDe* atomically in return less the gas & execution costs to execute the hedge.
2. Slippage & execution fees are included in the price when **minting** & **redeeming**. Ethena earns no profit from the **minting** or **redeeming of** *USDe*.
3. The protocol opens a corresponding short perpetual position for the approximate same notional dollar value on a derivatives exchange.
4. The backing assets are transferred directly to an "Off Exchange Settlement" solution. Backing assets remain onchain and custodied by off exchange service providers to minimize counterparty risk.
5. Ethena delegates, but never transfers custody of, backing assets to derivatives exchanges to margin the short perpetual hedging positions.

## Generated Revenue

The Ethena protocol generates three sustainable sources of revenue from the backing assets. 

The protocol revenue is derived from:

2. The funding and basis spread from the delta hedging derivatives positions.
5. The rewards earned from liquid stable backing assets.
8. Staked ETH assets receiving consensus and execution layer rewards.

Revenue from staked assets is floating by nature and denominated in the native asset - for example, liquid staked ETH tokens are typically denominated in *ETH*. 

The funding and basis spread can be floating or fixed depending upon if the protocol uses non-deliverable or deliverable derivatives positions to hedge the backing asset delta.

Rewards from liquid stables depends on where the assets are held and the rates offered by external stakeholders. These rates may vary based on the institution or platform managing the stables. For example, certain platforms may offer fluctuating interest rates on deposits, which can affect the overall returns.

The funding and basis spread has historically generated a positive return given the mismatch in demand and supply for leverage in crypto as well as the existence of positive baseline funding. 

If funding rates are deeply negative for a sustained period of time, such that the staked asset revenue cannot cover the funding and basis spread cost, the Ethena "reserve fund" is designed to bear the cost.

## Risks

2. Smart Contract Risk
5. External Platform Risk
8. Liquidity Risk
11. Custodial Operational Risk
14. Exchange Counterparty Risk
17. Market Risk

Ethena recognizes these risks and actively attempts to ameliorate & diversify these risks as much as possible. In practice, this means the system uses multiple providers for each step of the workflow and actively monitors all partners and market conditions. 

Every element of the Ethena design has been formulated with risk mitigation in mind including the use of custodians, absence of material leverage, and diversification constraints on the hedging positions

Last updated 5 months ago

Was this helpful?

---


# Overview

Source: https://docs.ethena.fi/backing-custody-and-security/overview

Last updated 6 months ago

Was this helpful?

---


# Custodian Attestations

Source: https://docs.ethena.fi/resources/custodian-attestations

Last updated 2 days ago

Was this helpful?

---


# How to [Un]lock positions

Source: https://docs.ethena.fi/video-guides/how-to-un-lock-positions

Users in permitted jurisdictions can **lock** & **unlock** positionswith Ethena via our UI.

Using the UI, the **locking & unlocking** positionsuser workflow is:

1. The user requests to **lock/unlock** positionsvia our dApp interface by clicking "Lock"/"Unlock", which pops up their selected wallet to sign the requested transaction.
2. After the user signs the transaction with their wallet, the transaction is submit to the blockchain, if successful, the cooldown period starts.
3. Once the cooldown period ends, the user now needs to click on "Withdraw" and sign a second transaction.
4. Upon successful confirmation of the transaction, the user receives unlocked tokens.

## Important to Note

* There is a cooldown period of 7 days after unlocking *USDe, USDe* will be available to withdraw after that period.
* There is a cooldown period of 7 days after unlocking *sENA, sENA* will be available to withdraw after that period. This is in addition to the 7 day sENA unstaking cooldown.
* There is a cooldown period of 21 days after unlocking LP tokens, these LP tokens will be available to withdraw after that period.
Last updated 6 months ago

Was this helpful?

---


# Underlying Derivatives

Source: https://docs.ethena.fi/solution-overview/underlying-derivatives

## Context

Ethena utilizes derivatives positions to buttress the synthetic USD value of the backing assets in most market conditions. This is achieved by being "delta neutral" through the use of an offsetting short derivatives position to the natural long spot position from backing assets.

In the subsections below, we go into what each term refers to and the key differences:

* Futures vs Perpetuals
* Inverse vs Linear Contracts
* Basis Spread

## Overview

Ethena trades derivatives across all major centralized exchanges that are supported by "Off-Exchange Settlement" providers.

At a high level, Ethena trades derivatives with a few motivations:

* Ethena opens a short position when a user **mints** *USDe*.
* Ethena closes a short position when a user **redeems** *USDe*.
* Ethena closes/opens positions across exchanges to realize unrealized PnL.
* Ethena algorithmically optimizes positions in the backing portfolio to account for risk.
* Ethena algorithmically optimizes positions in the backing portfolio to account for the differences between the exchanges' derivative contract specifications & the capital efficiency available from each exchange.

It is important to note that not all exchanges offer the same derivatives contracts and there are often key differences between each. Ethena is also sensitive to the exchange-assigned backing assets value when using liquid staking Ethereum assets, such as stETH, to margin ETHUSD or ETHUSDT Perpetual positions.

Last updated 6 months ago

Was this helpful?

---


# Peg Arbitrage Mechanism

Source: https://docs.ethena.fi/solution-overview/peg-arbitrage-mechanism

Last updated 9 months ago

Was this helpful?

---


# Scenario Analysis

Source: https://docs.ethena.fi/solution-overview/scenario-analysis

Given *USDe's* underlying peg stability mechanism is for the protocol to be long spot assets & short a derivatives position, a common question has been:

**"How does a change in the price of BTC affect the underlying backing composition?"**

This is a great question in that it allows discussion in more detail about the composition of assets in the Ethena backing in different BTC price scenarios.

---

## Overview

Given the protocol utilizes both inverse coin-margined and linear usd-margined contracts as well as trades across multiple exchanges, there are differences in how Ethena settles outstanding PnL. These differences stem from: 

* Each exchange's contract specifications, margining, and risk systems being subtly different.
* Inverse coin-margined contracts typically recording & settling PnL in base currency (eg BTC for BTCUSD Perpetual contracts) terms while linear contracts typically recording & settling in *USDT* (eg for ETHUSDT Perpetual contracts).

This brings up an important subject of "unrealized" and "realized" PnL.

* "Unrealized PnL" refers to when an existing position has incurred a profit or loss (difference between the average position price & the mark price of the contract), but the position has not yet been fully or partially closed. In essence, for example, the position has an outstanding profit/loss denominated in *BTC* or *USDT*, but this has not been received or paid from or to the portfolio's collateral balance.
* "Realized PnL" refers to when a part or all of a position has been closed and has received or paid the PNL to/from the collateral balance.

What this means is that Ethena typically receives/pays profit/loss in *BTC or USDT* depending upon the exchange and margin type of the positions the protocol is trading.

A change in the price of *BTC* does NOT mean the portfolio is immediately buying/selling collateral to meet unrealized PnL moment by moment.

As a result, this means that the portfolio at times has balances owed to it or owes in *BTC* or *USDT* terms. The ~USD value of the backing assets underpinning the synthetic dollar remains constant.

The protocol expects to be able to naturally "realize" "unrealized PnL" by:

* Closing existing positions when **redeem** *USDe* requests are received.
* Periodically rolling hedging positions between exchanges as it suits the risk & return framework.

---

## Scenarios

## BTC Price Decreases

In this scenario, the price of *BTC* decreases from when the positions were opened upon **minting** *USDe*. This means the portfolio's derivatives positions have unrealized profits across both inverse coin-margined & linear margined positions. These unrealized profits are denominated in BTC & *USDT*. Ethena has not sold or reduced the amount of backing assets the protocol is holding.

There is no significant drag to the portfolio's yield or risk by holding a small proportion of the portfolio in unrealized *BTC* or *USDT* terms.

Below are two examples demonstrating the impact of differing price scenarios upon inverse & linear contract margined positions. You'll notice the portfolio is able to either purely hold BTC to margin positions or is able to hold a proportion in the "Settlement Currency" (the motivations will be discussed further down).

You'll notice as the price of *BTC* continues to fall, a greater proportion of the protocol's backing assets value resides in the unrealized profit of the hedging position.

It's important to keep in mind the portfolio is automatically rebalanced by Ethena and the extreme, edge-case price scenarios are designed to demonstrate if rapid movements were to occur and the Ethena system were not to intervene. 

## BTC Price Increases

In this scenario, the price of *BTC* increases from when the positions were opened upon **minting** *USDe*. This means the portfolio's derivatives positions have unrealized losses across both inverse/coin-m & linear margined positions. These unrealized losses are denominated in *BTC* & *USDT*. Ethena has not sold or reduced the amount of backing assets the protocol is holding.

There is no significant drag to the portfolio's yield or risk by holding a small proportion of the portfolio in unrealized *ETH* or *USDT* terms.

It is important to note that the loss on the derivatives positions is perfectly offset by the gain in the value of the spot assets in normal market conditions. The ~USD collateral underpinning *USDe* generally remains constant in those environments.

One difference between the price of BTC increasing vs decreasing is that Ethena across many exchanges needs to be able to meet the unrealized loss with the "Settlement Currency" asset of the contract. The "Settlement Currency" asset of the contract is the asset in which PnL is settled. For example, for BTCUSDT Perpetual positions, PnL is settled in *USDT*. As such Ethena is able to:

* Maintain a balance of the "Settlement Currency" in the portfolio to meet this requirement.
* "Borrow" the balance from the exchange, at a reasonable variable interest rate, until the debt is extinguished (by acquiring the "Settlement Currency").

Below are two examples demonstrating the impact of differing price scenarios upon inverse & linear contract margined positions.

You'll notice as the price of *BTC* increases, a greater proportion of the protocol backing value resides in the spot Staked Ethereum asset with the unrealized loss in *BTC* or *USDT* terms growing.

It's important to keep in mind the portfolio is actively managed by Ethena & the extreme price scenarios are designed to demonstrate if rapid movements were to occur & Ethena were not to intervene. This is not a realistic assumption in reality.

---

## Scenario Consequences to the Portfolio

As you'll notice from the scenarios the examples above, there is benefit for the Ethena system to manage the composition of the portfolio as the *BTC* price changes. This management does not need to occur every 5/10/20% difference in price as the implications are related to economic efficiency rather than stability.

The natural **mint** & **redeem** *USDe* flow in combination with automated rebalancing ensures even in the most volatile markets the cost to the portfolio will be minimal & offset by the revenue generated.

---

## Further Notes

Given Ethena utilizes both inverse/coin & linear margined contracts, a question has been: **"What proportion of the portfolio is in USDT under different rapid price movements?"**

With the intention to keep this brief, you'll notice in the image below the scenarios wherein the portfolios has greater USDT exposure.

Given the protocol uses both inverse coin-margined contracts as well as linear usd-margined contracts, the proportion very much depends upon how much of the portfolio is hedged with either. As a protocol, we have a firm bias towards using inverse contracts. This is primarily a risk-related decision given it removes the reliance on USDT as well as because of its capital efficiency.

It's also important to note that the portfolio is actively managed & when the price of the underlying asset changes significantly, there is a greater likelihood that the positions will have already been rolled to realize the "unrealized PnL".

Last updated 3 months ago

Was this helpful?

---


# Delta-Neutral Stability

Source: https://docs.ethena.fi/solution-overview/usde-overview/delta-neutral-stability

Last updated 1 year ago

Was this helpful?

---


# Censorship Resistance

Source: https://docs.ethena.fi/solution-overview/usde-overview/censorship-resistance

## How *USDe furthers* censorship resistance

Assets backing USDe remain in "Off-Exchange Settlement" institutional grade solutions at all times. The only time collateral flows between custody and exchange is to settle funding or realized P&L.

Ethena utilizes "Off-Exchange Settlement" (OES) providers to hold backing assets. This enables Ethena to delegate/undelegate backing assets to centralized exchanges without being exposed to exchange-specific idiosyncratic risk.

While using an OES provider requires a technological dependence upon the OES provider, it does NOT mean counterparty risk has simply been transferred from the exchange to the OES provider. OES providers typically, where not using an MPC solution, employ a bankruptcy-remote trust framework to ensure the OES provider's creditors have no claim to the assets. In the case of an OES provider failing, these assets are expected to be outside the provider's estate and not exposed to the credit risk of the custodian. 

Empirically, Ethena's integrated providers for custody services have never lost a dollar of users funds compared to the $7bn lost in DeFi hacks, and >$15bn in CeFi insitutions last cycle.

Last updated 5 months ago

Was this helpful?

---


# Inverse vs Linear Contracts

Source: https://docs.ethena.fi/solution-overview/underlying-derivatives/inverse-vs-linear-contracts

## Inverse vs Linear Contracts

A linear payout is the simplest to describe and is used for many swaps. The price of a linear contract is expressed as the price of the underlying against the base currency. ETHUSDT is a linear perpetual and is quoted in Tether, with margin and PNL calculations denominated in Tether.

An inverse contract is worth a fixed amount of the quote currency. In the case of the ETHUSD perpetual, each contract is worth $1 of Ethereum at any price. ETHUSD is an inverse contract because it is quoted as ETH/USD but the underlying is USD/ETH or 1 / (ETH/USD). It is quoted as an inverse to facilitate hedging US Dollar amounts while the spot market convention is to quote the number of US Dollars per Ethereum.

## Convexity Implications

Convexity (also known as Gamma) refers to the second derivative of a contract's value with respect to price, and in the case of inverse perpetual futures, it can differ from the relationship suggested by a linear move in price.

While the payoff for a linear contract is just the Contract Multiplier\*(Entry Price-Exit Price), the payoff for an inverse contract is Contract Multiplier\*(1/Entry Price - 1/Exit Price), introducing convexity.

**Example**

A trader goes long 50,000 contracts of ETHUSD at a price of 10,000. 

A few days later the price of the contract increases to 11,000.

The trader’s profit will be: 50,000 \* 1 \* (1/10,000 - 1/11,000) = 0.4545 ETH

If the price had in fact dropped to 9,000, the trader’s loss would have been: 50,000 \* 1 \* (1/10,000 - 1/9,000) = -0.5556 ETH. 

The loss is greater because of the inverse and non-linear nature of the contract. 

Conversely, if the trader was short then the trader’s profit would be greater if the price moved down than the loss if it moved up.

Last updated 1 year ago

Was this helpful?

---


# Basis Spread

Source: https://docs.ethena.fi/solution-overview/underlying-derivatives/basis-spread

## What is a basis trade?

A basis trade is a trade in which the trader simultaneously purchases (sells) an asset and sells (buys) the futures contract for that asset. Since spot and futures are traded separately, their prices are not guaranteed to be the same at all times. In fact, their prices often diverge and this differential is known as the "basis".

As the future approaches expiration, its price often trends towards the underlying spot price. At expiration, futures contracts require the trader long the contract to purchase the underlying asset at the contract’s predetermined price, guaranteeing that at the futures contract expiry. Therefore, as the futures expiration draws nearer, the basis should approach 0. 

If for example, the futures contract is trading at a premium to the underlying spot price, a trader can short this future against the underlying and as the future converges to the spot price at expiration they will collect this difference in basis. Fixed expiry futures will provide a fixed interest rate on this basis trade.

**Example**

For instance, as of January 2025, the price for the **BTC/USD** spot was $103,337 whereas the price for the BTC March 28th expiry futures, has a price of $103,401. We define the basis as being the difference between the spot price and the futures price. 

The basis has a value of $103,401 - $103,337 = $64.

Last updated 3 months ago

Was this helpful?

---


# Custodial Risk

Source: https://docs.ethena.fi/solution-overview/risks/custodial-risk

## Context

Given that Ethena relies upon "Off-Exchange Settlement" provider solutions to hold protocol backing assets, there is a dependence upon their operational ability. This is the "Custodial Risk" we are referring to.

Counterparty risk is a prevalent issue throughout crypto and has never been more important than it is today. The custodians' business models are built on the safeguarding of assets, vs. the alternative of leaving backing assets sitting on a centralized exchange.

## Overview

There are three principal risks with using an Off-Exchange Settlement provider for custody:

1. **Accessibility and Availability.** Ethena’s ability to deposit, withdraw, and delegate to & from exchanges. Any of these abilities being unavailable or degraded would impede the trading workflows & availability of the **mint**/**redeem** *USDe* functionality.

	* It is important to note that this should NOT affect the value of the backing underpinning *USDe*.
2. **Performance of Operational Duties.** In the event of an exchange failure, the protocol is reliant upon cooperation and reasonable legal behaviour to facilitate the expedient transfer of any unrealized PnL at risk with an exchange. Ethena mitigates this risk by settling PnL with exchanges frequently to avoid large balances being owed to the protocol.

	* For example, Copper's Clearloop settles PnL between exchange partners and Ethena daily.
3. **Operational Failure of Custodian.** While the core team is not aware of any material operational failures or insolvencies for large-scale crypto custodians, this does remain a possibility. While assets are held in segregated accounts, insolvency of a custodian would pose operational issues for the creation and redemption of *USDe* as Ethena manages the transfer of assets to alternative providers.

	* Backing assets within these solutions are not owned by the custodian nor is the custodian or its creditors expected to have a legal claim on the assets. This is a result of OES providers either utilizing bankruptcy-remote trusts or MPC wallet solutions.

These three risks are mitigated by Ethena not exposing too much backing assets to a single OES provider and ensuring concentration risk is managed. It’s important to keep in mind that the system strives to use multiple OES providers with the same exchanges to mitigate both of the aforementioned risks.

## Example: Copper Clearloop

Individual custodial providers also provide the following protection, using Copper's Clearloop as an example:

* Copper has never been hacked or lost users’ funds in contrast to the $7bn lost in DeFi.
* Copper users’ funds were wholly available within days of Coinflex’s (exchange) failure.
* Copper users’ funds are a part of a bankruptcy-remote trust, meaning in the event of Copper’s failure, users’ funds are not a part of the Copper estate.
* Exchanges post collateral with Copper ahead of time to ensure users’ PnL is settled each cycle. This enables Copper to ensure users receive their PnL even if an exchange refuses to settle.
* Ethena retains the ability to dispute erroneous exchange settlement requests.

For more information, please refer to Copper's one-pager on Clearloop:

[2MBCopperClearloopOnePager.PDFpdf](https://596495599-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FsBsPyff5ft3inFy9jyjt%2Fuploads%2FsDzrtEQJW9WaoJfha374%2FCopperClearloopOnePager.PDF?alt=media&token=c8d75a40-8aa1-4055-980a-2c4405c5faf4)Last updated 6 months ago

Was this helpful?

---


# Exchange Failure Risk

Source: https://docs.ethena.fi/solution-overview/risks/exchange-failure-risk

## Context

Ethena utilizes derivatives positions to offset the delta of the protocol backing assets. These derivatives positions are traded upon CeFi exchanges such as Binance, Bybit, Bitget, Deribit, and Okx. As such, in the event an exchange were to suddenly become unavailable such as FTX, Ethena would need to manage the consequences. This is the "Exchange Failure Risk" we are referring to.

Protocol backing is NEVER deposited to exchanges and always resides with "Off Exchange Settlement" providers. Ethena has made significant efforts to minimize exposure to exchange failures.

## What happens in the event of a failure of an exchange?

Ethena retains complete control and ownership of the assets via Off-Exchange Settlement providers with no backing assets ever being deposited with any exchange. This limits Ethena's exposure to idiosyncratic events on any one exchange to the outstanding PnL between Off-Exchange Settlement providers' settlement cycles.

> Copper's Clearloop runs a settlement cycle daily.
> 
> 

As such, in the event of an exchange failure, Ethena would delegate the backing assets to another exchange and hedge the outstanding delta that was previously covered by the failed exchange. In the event of an exchange failure, the derivatives positions are considered closed with Ethena holding/owing no further obligation to the exchange estate.

Capital preservation is front of mind for Ethena. In the event of extreme circumstances, Ethena will always work to protect the value of the backing assets & *USDe* stable peg.

## How is the exchange failure risk managed?

As with all parts of Ethena' workflows, Ethena is agnostic to each provider at each step of the workflow. 

* Ethena diversifies the risk and mitigates the potential impact of exchange failure by utilizing multiple exchanges.
* Ethena is continually integrating with new sources of liquidity in an effort to limit the protocol's exposure to each source.
* Ethena actively monitors the ecosystem with investors, advisors, and friends across the industry, taking a proactive approach to de-risking exchange exposure if associated risks are perceived to have changed.

Ethena's strategy involves a portfolio allocation across different instruments and venues:

* 7% liquid cash (no intraday risk)
* 3% deliverable futures
* 90% perpetual futures, allocated as:

	+ **Binance** (50%): Daily settlement, 3 funding cycles
	+ **Bybit** (25%): 2-hour settlement, 1 funding cycle
	+ **OKX** (15%): 4-hour settlement, 1 funding cycle
	+ **Deribit** (5%): Daily settlement, 3 funding cycles
	+ **Bitget** (5%): 4-hour settlement, 1 funding cycle

Last updated 3 months ago

Was this helpful?

---


# Margin Collateral Risks

Source: https://docs.ethena.fi/solution-overview/risks/margin-collateral-risks

Ethena uses both linear and inverse margined perpetual futures, using linear perpetual futures that are denominated in USDT. Denominating in Tether means that the margin and PNL calculations are quoted in Tether, and by extension, results in Ethena being positionally long USDT.

For example, if Ethena posts BTC as margin collateral, and takes a short position on a linear BTC/USDT perpetual future - Ethena has a delta of 0 on BTC due to being long spot (collateral) and short futures (perpetual), but it is directionally long USDT (quote currency) with no offsetting short exposure. 

The inherent risk this presents is exposure to a potential USDT idiosyncratic event. 

For context, 80% of perpetual futures open interest is stablecoin-margined, with the vast majority of those quoted in USDT. 

Ethena closely monitors USDT stablecoin price risk and solvency, and if a problem persists will take action accordingly. In this instance, Ethena would aim to move more of the perpetual futures positions into inverse contracts, margined with BTC or ETH, depending on liquidity.

Last updated 3 months ago

Was this helpful?

---


# Risk Committee

Source: https://docs.ethena.fi/solution-overview/governance/risk-committee

The Risk Committee’s mandate is to generally identify, evaluate, and manage risk within the ecosystem

## Members

With regards to the Risk Committee, every 6 months, the initial terms for 3 out of 6 members of each committee will lapse, and their positions will be put up to governance via broad vote for either (i) confirmation for another term or (ii) to be filled by a replacement member.

For the first six month term, the Risk Committee members are as follows:

* Gauntlet​
* Block Analitica​
* Steakhouse
* Blockworks Research
* LlamaRisk
* Ethena Labs Research

ENA holders with more than 1,000 $ENA may nominate potential committee members in the governance forums. If the potential committee member accepts the nomination, the members of the Committee upon which a seat is being filled will conduct a confirmation vote after satisfying themselves regarding the suitability of the nominated candidate. A nominee advancing past the foregoing stages will then be subject to KYC/KYB screening by the Ethena Foundation, and if it passes those checks, will be included in the broader governance vote for the open Committee seats. The two nominees that garner the most votes will be named to the relevant Committee and execute a Governance Committee Service Agreement with the Ethena Foundation, which outlines the rights, obligations, compensation, and other terms associated with serving on the relevant Committee. A template of the Governance Committee Service Agreement will be published for public reference.

Committees will hold regular meetings as determined by the members, with support from the Ethena Foundation.

## Committee Decisionmaking Procedure

A member of a Committee wishing to make a specific change is required to propose the particular changes or decisions in the governance forums located at gov.ethenafoundation.com Following posting, a seven-day deliberation period begins, during which the members of the relevant Committee discuss the merits of the proposal. At the end of the deliberation period, a vote will be held amongst all voting members of the Committee. All changes require unanimous approval of the voting members.

If the proposal successfully passes, the Committee will instruct the relevant parties to implement the decision, subject to oversight by the Foundation. If the proposal is defeated, unless no Committee member other than the member who made the initial proposal votes in favor, Committee members who vote against the proposal are encouraged to provide a detailed response as to its rationale, and, if relevant, proposed amendments to the proposal it would suggest, to support the possibility of reaching consensus. 

Committee members are required to recuse themselves from the decisionmaking process with respect to proposals in which they have a direct financial interest - namely, where a product or service offered by the member is implicated by a proposal whereby the member stands to gain financially. 

## Ethena Labs Research

Ethena Labs Research will sit on the committee initially as a nonvoting member (though it may make proposals) and will receive no compensation. Its seat will be subject to confirmation or replacement at the conclusion of its term as any other member. If replaced, the replacement member will become a voting member. 

Last updated 8 months ago

Was this helpful?

---


# Reserve Fund

Source: https://docs.ethena.fi/solution-design/reserve-fund

The reserve fund acts as an additional margin of safety behind *USDe* to provide a source of capital to pay for periods of negative funding, as well as a bidder of last resort for *USDe* in open markets.

## Composition of Reserve Fund

Stable uncorrelated backing assets to cover funding payments in same currency denomination:

* Stablecoin assets including USDC and USDT for USD-M contracts
* Smaller ETH backing assets allocation for ETH-M contracts
* Other assets as determined by governance

## Security of Reserve Funds

Controlled by 4/8 multi-sig with keys held by contributors sitting within Ethena Labs.

## USDe Open Market Arbitrage Vehicle

Since the solvency of *USDe* is both transparent and provable during all periods of time, if the open market price of *USDe* diverges sufficiently from the provable asset value backing *USDe* in an extreme case then the reserve fund may act as a bidder of *USDe* in the open market.

## Capitalization of Reserve Fund

The reserve fund is funded with a portion of the revenue generated by the Protocol, allowing it to grow alongside the backing of *USDe*. The amount of Protocol revenue applied towards the reserve fund is subject to governance.

The reserve fund will also be capitalized with funds raised from private placement investors.

## Sizing

Ethena Labs conducted detailed modelling in November 2023 on the proposed sizing of the reserve fund under various stressed scenarios to inform the ongoing capitalization of the reserve.

The model tested out various assumptions using a $20m fund size. To note, the Reserve Fund size is $46.6m as of Q4 2024.

Last updated 3 months ago

Was this helpful?

---


# Key Addresses

Source: https://docs.ethena.fi/solution-design/key-addresses

Last updated 3 days ago

Was this helpful?

---


# Matrix of Multisig and Timelocks

Source: https://docs.ethena.fi/solution-design/key-trust-assumptions/matrix-of-multisig-and-timelocks

> Ethena is required to implement safeguards in order to provide connective tissue between DeFi and centralized liquidity venues. The multisig is used to minimize these trust assumptions for core onchain functions.
> 
> 

 

**Roles**

**Multi sig**

**Number of role**

**Functions**

**Notes**

**Owner**

Yes, Ethena org

1

transferOwnership, add/remove supported collateral asset, add/remove custodian addresses, setUSDe address

If desired, owner and admin can be different multi sigs

setUSDe address is redundant, to be removed

**Admin**

Yes, Ethena org

1

grant/revoke Minter, Redeemer, Gatekeeper roles

 

**Gatekeepers**

No, EOA controlled by Ethena plus external trusted organisations

At least 3

Disable mint/redeem functionality, remove Minter, Redeemer roles

Will include external trusted organisations to be gatekeepers. Limits damage on mint/redeem roles compromise. Disables mint/redeems when they execute at incorrect prices on chain.

**Minter**

No, EOA controlled by Ethena

20

* `mint()`
* `transferToCustody`
Mint/Redeemer roles to be the same set of 20 addresses. This is to ensure the system can handle a high load of mint transaction concurrently.

**Redeemer**

No, EOA controlled by Ethena

20

* `redeem()`
Mint/Redeemer roles to be the same set of 20 addresses. This is to ensure the system can handle a high load of mint transaction concurrently.

Last updated 1 year ago

Was this helpful?

---


# User Security Measures

Source: https://docs.ethena.fi/solution-design/minting-usde/user-security-measures

## Overview

Several measures have been taken to ensure the integrity and resilience of the deployed smart contracts. These measures are designed principally to ensure the safety of protocol assets, but also to ensure reasonable governance occurs.

Below is a list of some, but not all, of the user security measures Ethena has implemented across the deployed smart contracts.

## Measures

1. Only whitelisted user wallet addresses are able to successfully **mint** & **redeem** *USDe*. This seeks to ensure that only non-malicious actors are able to call the aforementioned functions.
2. Provided backing assets are only able to be sent from the Ethena Minting contract to whitelisted wallet addresses of our OES provider partners. This ensures protocol backing is not able to be diverted to improper wallets and protocol funds enjoy the legal and governance protections without interruption.

	* Updating the whitelisted addresses in the Ethena Minting contract requires a multi-sig transaction by members of both Ethena & external responsible parties.
3. Mint/Redeem Smart contract keys are generated in an air-gapped secure manner whereby a single person is not able to access these keys.
4. A small proportion of the protocol's total assets are kept in EOA wallets. Secure multi-sig approval process is required for major fund transfers.
5. Internal pricing sourced from multiple centralized exchanges is constantly validated with external sources such as Pyth and Redstone to ensure integrity.
6. Numerous [Order Validity checks](/solution-design/minting-usde/order-validity-checks) are performed throughout the system + workflow to ensure the integrity of the system.
7. Separate `GATEKEEPER_ROLE` roles across the smart contract exist to detect unusual **mint**/**redeem** transactions and immediately disable the mint/redeem functionality upon unexpected behavior.
8. The `DEFAULT_ADMIN_ROLE` and `owner` smart contract roles are all multi-sig keys and are securely stored in cold wallets.

**Security Measure**

**Action Taken by Ethena**

**Purpose & Benefit**

**Handling of Mint/Redeem Keys**

Ethena securely generated mint/redeem keys are stored safely in AWS secrets manager. Exist on production machines upon deployment only which has critically restricted access.

Ensures no unauthorized access, safeguarding users and the protocol from potential mint/redeem key compromises.

**Address Validity**

Only whitelisted addresses can receive backing assets. Withdrawals restricted to whitelisted custodian addresses.

Minimises risk of sending funds to incorrect addresses, ensuring targeted and secure end to end mint/redeem flows.

**On-Chain Fund Management**

Avoid keeping large sums in EOA wallets. Secure multi-sig approval process for major fund transfers.

Safeguards protocol assets and protects from unintended fund movements.

**Ensuring Correct Pricing**

Validate internal pricing consistently against third-party sources. Real-time checks and balance measures.

Accurate pricing is essential, ensuring users get the best value and protocol remains stable.

**Hedging Processes**

Robust checks and balances for hedging, including block number validations and system health checks.

Ensures orders are handled correctly and reliably, minimising potential order execution errors.

**Protecting against Adverse Selection**

Employ a last-look architecture, whitelist market makers, and set tight windows for quote validity.

Priorities giving users the best pricing and protects against potential manipulations or unfair play.

**Gas Estimation**

Maintain a limited ETH balance for transactions and monitor gas fees to prevent overpayment.

Ensures users are not overcharged due to gas estimation errors, preserving user funds.

**Strict Order Submission**

Only whitelisted users can submit orders, which must meet Ethena’s validation criteria.

Protects the system against malicious public internet orders, only genuine requests are processed.

**Robust Role Management**

Distinct gatekeeper roles for monitoring and managing unusual mint/redeem transactions.

Specialised roles allow for targeted oversight and faster response to potential security threats.

**Cold Storage of Multi-Sig Keys**

Admin and owner multi-sig keys of all contracts are securely stored in cold wallets.

Enhances security by reducing exposure of essential keys to online threats.

Last updated 9 months ago

Was this helpful?

---


# Mint & Redeem Key Functions

Source: https://docs.ethena.fi/solution-design/minting-usde/mint-and-redeem-key-functions

## Roles in EthenaMinting contract

## Overview

The Ethena minting contract has been designed to offer a safe and secure platform for the creation of *USDe*. Its atomic operations ensure that tasks are either fully completed or reverted, leaving no room for partial executions. Its immutable nature guarantees that its critical rules and operations cannot be easily altered, ensuring consistency and trust in the process. It has these key pieces of functionality:

1. **Minting**: Minters can mint *USDe* by providing assets and receiving *USDe* tokens in return. The backing assets are transferred to "Off-Exchange Settlement" providers based on a predefined route. The minting process is subject to a maximum limit set by the contract.
2. **Redemption**: Redeemers can redeem their *USDe* by providing them as input and receiving the underlying assets back *USDe* in return. The redeemed *USDe* tokens are burned from the user's balance. The redemption process is subject to a maximum limit set by the contract.
3. **Signature Verification**: The contract cryptographically verifies the signature provided by the user to ensure the authenticity of the minting or redemption order.
4. **Supported Assets:** The contract maintains a strict list of supported assets that can be used as backing assets for minting and redemption.
5. **Custodian Addresses:** The contract maintains a strict list of custodian addresses to which backing assets can be transferred during the minting process.
6. **Max Mint/Redeem Per Block:** The contract sets a maximum limit for the number of *USDe* tokens that can be minted or redeemed per block.

Roles in smart contracts are what control lower level operations and function calls. It's a security feature, like AWS IAM, that allows the authors of smart contracts, and the users using them once deployed to the blockchain, to be certain of how they can operate.

Despite being named the "Ethena Minting contract", it is responsible for both the **minting** & **redeeming** functionality of *USDe*.

## Roles in the Ethena Minting contract

There are five roles in the Ethena Minting contract. You can view the deployed Ethena Minting contract on the Ethereum blockchain **here**.

RoleTypeControllerRole CountFunctions / Notes`ADMIN`

Multi-Sig

Ethena Labs

1

* Transfer Ownership
* Add/remove supported collateral asset
* Add/remove custodian addresses
* Grant/revoke Minter, Redeemer, Gatekeeper roles
* Set max/mint mint/redeem per block
* Reenable mint/redeem

`GATEKEEPER`

EOA

Shared between

* Ethena Labs
* External Security Firms

3+ internal 3+ external

* Disable mint/redeem

	+ Disables when they execute at incorrect prices on chain
	+ Limits damage on mint/redeem roles compromise

`MINTER`

EOA

Ethena Labs

20

* Mint
* Transfer to approved "Off-Exchange Settlement" providers

`REDEEMER`

EOA

Ethena Labs

20

* Redeem

## 

Last updated 1 year ago

Was this helpful?

---


# Internal Services

Source: https://docs.ethena.fi/solution-design/hedging-system/internal-services

At a high level, the "Hedging System" is composed of broadly five services:

1. **Portfolio Management System**
2. **Market Data Parser Service**
3. **Reference Data Service**
4. **Reconciliation Service**
5. **Persistor Service**

## **Services**

## **Portfolio Management System**

The "Portfolio Management System" manages a number of key functions including:

* Calculating and publishing indicative prices if users were to **mint** & **redeem** *USDe*.
* Calculating and publishing prices for users' **mint** & **redeem** *USDe* requests.
* Calculating portfolio exposure in real time & requesting operations as a result.
* Orchestrating the delegation/undelegate between "Off-Exchange Settlement" providers and CeFi exchanges as well as coordinating the movement of backing assets between "Off-Exchange Settlement" providers & Minting + Staking smart contracts.
* Routing and managing the execution of orders to manage risk.
* Altering in the event of system degradation or inconsistency present in the system.

## **Market Data Parser Service**

The "Market Data Parser Service" connects & ingests market data updates from CeFi Exchanges, "Off-Exchange Settlement" providers, as well as Pyth and Redstone. This information includes order book updates, public trades, and private orders, positions & trade information.

The application is designed, built, and deployed in a manner wherein it is resilient and functional even in high-volatility environments.

*When does Ethena consider external market data invalid?*

We capture invalid data in two dimensions:

* Wrong/invalid
* Outdated

Data directly from exchanges gets compared against Pyth and has to fall within a tight tolerance, which is manually set but wide enough to allow even rapid moves. It's mainly trade-through events; one large order walks 50 levels into the order book, which we would like to avoid reacting on.

During volatile moments, the exchanges tend to fall behind on their updates. We have spent extensive engineering resources to deal with such situations (efficient data reading from network card, batch processing, update filtering etc.) to avoid being the bottleneck.

We have continuous time synchronisation between our system and the connected exchanges. Once we detect a time drift of the updates published (set either by the exchange gateway or matching engine, depending on the exchange), we update our RFQ look-back period to reflect this. This means that we only give the final acceptance of the RFQ once we have the up-to-date market data. This mechanism is vital to protect the protocol against adverse selection by market makers with faster infrastructure.

In case the market data falls further behind our suspend threshold, we put the instrument into suspend mode. The latency has to improve significantly for the instrument to be enabled again, as it requires passing a hysteresis -this avoids on/off flickering.

## **Reference Data Service**

The "Reference Data Service" normalizes & validates the integrity of all ingested data.

## **Reconciliation Service**

The "Reconciliation Service" periodically verifies information throughout the system is consistent with that from external sources. This includes, but not is not limited to position & market data information. This service is one of many layers throughout the system to validate & ensure the integrity of the operation of the system.

## **Persistor Service**

The "Persistor Service" publishes internal events to data stores, such as databases. This enables recovery in a wide range of instances without losing data & enables Ethena to rapidly heal and continue operations without interruption or user detriment.

Last updated 6 months ago

Was this helpful?

---


# Managing Risk from dependencies

Source: https://docs.ethena.fi/solution-design/hedging-system/managing-risk-from-dependencies

Ethena Labs' "Hedging System" has three notable external dependencies (aside from AWS):

1. CeFi Exchanges, such as Bybit.
2. "Off-Exchange Settlement" (OES) providers, such as Copper.
3. Price Feeds, such as Pyth and Redstone.

It is important to note that Ethena Labs has team members available 24/7 across different timezones & countries who are able to manage and address any issues that might occur.

If any of the system checks performed both internally and externally by market making entities with gatekeeper roles can disable the ability to **mint** & **redeem** *USDe* until they are satisfied the system is functioning correctly without discrepancies.

## Possible Negative Events

The following is a list of negative events that might occur, what the issue to the system would be, how it is mitigated/ameliorated, and the maximum potential impact to the protocol.

> Note: This is not an exhaustive list, but the most common & likely (in the unlikely event they occur).
> 
> 

## CeFi Exchange / OES Partner suffers technical issues

Where a CeFi Exchange or OES partner suffers technical issues such as failing to send real-time updates or perhaps inconsistent information per their specification across multiple objects; this would cause internal objects to not match the system's expectations.

As a result, the system would immediately identify this inconsistency and determine if it is isolated to a single partner. If it's possible to continue **minting** and **redeeming** *USDe* while quarantining the affected partner(s), the system will; if not, **minting** and **redeeming** *USDe* will be paused until the issue can be addressed.

The system identifies these inconsistencies by performing a large number of validations upon data in real-time, with constant reconciliation with partners, and alerting.

## CeFi Exchange(s) becomes temporarily inaccessible

In the event a CeFi Exchange partner(s) were to become temporarily inaccessible, Ethena would no longer be able to submit or edit existing orders on exchanges. This would result in Ethena losing control of any existing orders & possibly being able to reconcile the exact state of that exchange's portfolio.

The system would immediately identify this issue and attempt to cancel all outstanding open orders on the exchange. The system would attempt to identify the latest portfolio update and would no longer attempt to submit new orders. The system would distribute hedging orders to other exchange partners and only include the affected partner(s) again when service had been satisfactorily restored.

Availability and integrity are considered in a wide range & number of validations that are constantly performed throughout the system.

## Market Data prices lack integrity

In the event some or all market data price feeds begin to lack integrity, Ethena would immediately cancel all affected open orders and identify the affected partners. The lack of market data would prevent Ethena from being able to submit orders to exchange partners.

It's important to keep in mind that Ethena is integrated with multiple market data feeds & exchange prices as to ensure the affected partner(s) can be quarantined without damaging the integrity of operations.

The "Hedging System" monitors for integrity in real-time and actively alerts in the event of any concerns.

## Internal System component fails

In the event that an internal system service fails, becomes unresponsive, or begins to behave in an inconsistent manner, the system identifies and quarantines the issue in real-time.

The system has been designed to self-heal in the event of any failures or degradations as well as there is a large focus throughout the system upon ensuring each interaction & data stored makes "sense".

The system is actively tested end to end, in addition to unit/component/integration tests, as well as ensuring there is alerting throughout the system that readily notifies the appropriate parties.

In the event a service fails and is unable to self-heal, **minting** and **redeeming** *USDe* is automatically temporarily paused while the outstanding issue is investigated & resolved.

Last updated 6 months ago

Was this helpful?

---


# USDe + sUSDe Custodian Availability

Source: https://docs.ethena.fi/resources/usde-+-susde-custodian-availability

Last updated 2 months ago

Was this helpful?

---


# Audits

Source: https://docs.ethena.fi/resources/audits

Last updated 1 month ago

Was this helpful?

---


# General Risk Disclosures

Source: https://docs.ethena.fi/resources/general-risk-disclosures

Please consider information in this Risk Disclosure Statement (“Statement”) as a general overview of the risks associated with the services offered by Ethena Labs and its affiliates (the “Services”) made for your awareness only. We do not intend to provide investment or legal advice through this Statement and make no representation that the Services described herein are suitable for you or that information contained herein is reliable, accurate or complete. We do not guarantee or make any representations or assume any liability regarding financial results based on the use of the information in this Statement, and further do not advise to rely on such information in the process of making a fully informed decision whether or not to use the Services. The risks outlined in this Statement are not exhaustive and this Statement only outlines the general nature of certain risks associated with crypto assets, and does not discuss in detail all risks associated with holding or trading crypto assets. Users should undertake their own assessment as to the suitability of using crypto assets and associated Services based on their own investigations, research and based on their experience, financial resources, and goals. You should not deal with crypto assets unless you understand their nature and the extent of your exposure to risk.

Note that specific disclosures and terms of service will apply with respect to various offerings of Ethena Labs, which will be published separately. Users should refer to those terms in addition to the disclosures herein when deciding whether to utilize the Services.

For the purpose of this Statement “you”, “your”, and “User” mean a user of our services and “we”, “us”, “our”, or “Ethena”, mean Ethena GmbH and Ethena (BVI) Limited. Users are strongly advised to read this Risk Disclosure Statement carefully before deciding to start using the Services.

RISK OF LOSS IN TRADING CRYPTO ASSETS CAN BE SUBSTANTIAL AND YOU SHOULD, THEREFORE, CAREFULLY CONSIDER WHETHER SUCH ACTIVITY IS APPROPRIATE FOR YOU IN LIGHT OF YOUR CIRCUMSTANCES AND FINANCIAL RESOURCES. YOU SHOULD BE AWARE OF THE FOLLOWING:

**Crypto Assets Are Not Legal Tender In Most Jurisdictions**

Most crypto assets are not backed by any central government or legal tender (except in few, discrete cases), meaning each country has different standards. There is no assurance that a person who accepts crypto assets as payment today will continue to do so in the future. Holders of crypto assets put their trust in a digital, decentralized, and partially anonymous system that relies on peer-to-peer networks and cryptography to maintain its integrity, and neither vendors nor individuals have an obligation to accept crypto assets as payment in the future;

**Loss of value, Volatility and Uncertainty of Future Performance**

There is typically limited or no fundamental reasoning behind the pricing of crypto assets, creating the risk of volatility and unpredictability in the price of crypto assets relative to fiat currencies. Crypto assets have had historically higher price volatility than fiat currencies, including irrational and extreme moves in price as the process for valuation can be speculative and uncertain.

**Liquidity Risk**

Crypto assets can have limited liquidity that can make it difficult or impossible to sell or exit a position when desired. This can occur at any time, especially during periods of high volatility.

**Dual-issuer Risk (only with regard to USDe)**

There is a risk that Ethena (BVI) Limited may not be able, temporarily or permanently, to rebalance all or part of its reserve assets to the reserve of assets of Ethena GmbH within the meaning of Article 3 para. 1 no. 32 Regulation (EU) 2023/1114 of the European Parliament and of the Council of 31 May 2023 on markets in crypto-assets (“MiCAR”) in the event that holdings and redemptions of USDe shift significantly towards the European Economic Area (“EEA”), impacting Ethena GmbH’s ability to cover its liability towards EEA holders of USDe. Likewise, there is a risk that Ethena GmbH may not be able, temporarily or permanently, to rebalance all or part of its reserve of assets to Ethena (BVI) Limited’s reserve assets, impacting Ethena (BVI) Limited’s ability to cover redemption obligations to non-EEA holders of USDe.

**Market forces**

Trading in crypto assets may be susceptible to irrational market forces, such as speculative bubbles, manipulation, scams, and fraud.

**Financial Crime and Cyber Attacks**

Cyber crime relating to crypto assets can be more prevalent than other financial crime as the ecosystem is totally digital and traditional governance and risk mitigants may be lacking. For example, a 51% attack is an attack on a blockchain by any person or group of persons who control more than 50% of the network. Attackers with majority control of a network can interrupt the recording of new blocks, alter payment history, and subvert funds. Users are susceptible to malware and fake/hijacked addresses and other forms of cyber-attacks and Users should always take care of passwords and double check the addresses and URLs before loading software or interacting with any platform, protocol, or service.

**Absence of Control**

Ethena is not a broker, agent or advisor and has no fiduciary relationship or obligation to Users in connection with any transaction or other decision or activity undertaken by you using the Services. We do not control whether your use of the Services is consistent with your financial goals. It is up to Users to assess whether their financial resources are appropriate for their respective activity with us and risk appetite in the products and services you use.

**Availability of Services**

We do not guarantee that the Services will be available at any given time or that the Services will not be subject to unplanned service interruptions or network congestion. You may not be able to buy, sell, store, transfer, redeem, send, or receive crypto assets when you want to.

**Technology Risk**

The risks of crypto assets being transacted via new technologies (including distributed ledger technologies) include, among other things, anonymity, irreversibility of transactions, accidental transactions, transaction recording, and settlement. Transactions in crypto assets on a blockchain relies on the proper functioning of complex software, which exacerbates the risk of access to or use of crypto assets being impaired or prevented. Moreover, there is risk of failures, defects, hacks, exploits, protocol errors, or unforeseen circumstances that might occur in connection with a crypto asset or the technologies on which the crypto asset is based.

**Irreversible Transactions**

Transactions in crypto assets are generally irreversible. As a result, losses due to fraudulent or accidental transactions may not be recoverable.

**Third Party Risk**

Third parties such as payment providers, custodians, exchanges, and banking partners may be involved in the provision of the Services. You may be subject to the terms and conditions of these third parties, and Ethena cannot be responsible for any losses these third parties may cause you.

**Taxation and Disclosure of Information**

You are responsible for determining the taxes to which you may be subject and their application when using the Services. It is your responsibility to report and pay any taxes that may arise from transactions and you acknowledge that Ethena does not provide legal or tax advice regarding such transactions. If you have concerns about your tax treatment or obligations you may wish to seek independent advice.

You understand that when, where, and as required by applicable law, Ethena will disclose available information relating to transactions transfers, distributions or payments to the appropriate regulatory and tax authorities or other public authorities. Similarly, when, where and as required by applicable law, Ethena will withhold taxes related to your transactions, transfers, distributions or payments.

**No Investment and Legal Advice**

Communications or information provided by Ethena shall not be considered or construed as investment advice, financial advice, trading advice, or any other type of advice. The User is the only party who can determine whether an investment, investment strategy or related transaction is appropriate based on his or her personal investment objectives, financial situation and risk tolerance, and shall be solely responsible for any losses or liabilities that may result.

**Regulatory Risk**

The regulation of crypto assets and platforms is uncertain in many jurisdictions and Ethena cannot be held responsible for compliance with legal rules of countries from which customers, on their own initiative, access the Services. Moreover, changes in rules applicable to crypto assets may considerably impact on the prices of those assets and are unpredictable. You further acknowledge the above list of risks is non- exhaustive and there may also be unpredictable risks.

Last updated 4 months ago

Was this helpful?

---


# Privacy Policy

Source: https://docs.ethena.fi/resources/privacy-policy

Last Revised on January 2025

This Privacy Policy for Ethena GmbH, represented by the managing directors Torsten Luettich and Guy Young, Friedrich-Ebert-Anlage 49, 60308 Frankfurt am Main, and Ethena (BVI) Limited (collectively, "Company", "we", "us" "our") describes how we collect, use and disclose information about users of the Company's websites (ethena.fi and ethena.gmbh, the “Site”), and any related services, tools and features, including the Ethena service (collectively, the "Services"). For the purposes of this Privacy Policy, "you" and "your" means you as the user of the Services. Please read this Privacy Policy carefully. By using, accessing, or downloading any of the Services, you agree to the collection, use, and disclosure of your information as described in this Privacy Policy. If you do not agree to this Privacy Policy, please do not use, access or download any of the Services. ​

## UPDATING THIS PRIVACY POLICY

We may modify this Privacy Policy from time to time in which case we will update the "Last Revised" date at the top of this Privacy Policy. If we make material changes to the way in which we use information we collect, we will use reasonable efforts to notify you (such as by emailing you at the last email address you provided us, by posting notice of such changes on the Site, or by other means consistent with applicable law) and will take additional steps as required by applicable law. If you do not agree to any updates to this Privacy Policy please do not access or continue to use the Services. ​

## COMPANY'S COLLECTION AND USE OF INFORMATION

​When you access or use the Services, we may collect (directly or through third-party providers) certain categories of information about you from a variety of sources, which comprises: ​

* Information provided during “Know Your Customer” (“KYC”) and Anti-Money Laundering (“AML”) processes, which includes personal identifying information. This may include:
* Basic Information: Name, Address, Date of Birth, Nationality, Country of Residence, Phone Number, Email Address.
* Identification Information: Utility bills (or other proof of address), photographs, Government-issued identification (such as identification cards, passports, driver’s licenses, etc.), tax ID number, employment information, proof of residency, visa information, organizational documents, and information regarding ultimate beneficial owners.
* Financial Information: Income/net assets/wealth verification statements.

We process the data provided and collected to provide the Services, personalize your experience with the Services, and improve the Services. Specifically, we use your data to:

* identify you as a user in our system;
* identify your place of residence, or registered office;
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

## HOW THE COMPANY SHARES YOUR INFORMATION

​In certain circumstances, the Company may share your information with third parties for legitimate purposes subject to this Privacy Policy. Such circumstances comprise of: ​

* Blockchain analysis service providers, including TRM​ (TRM is a member of the EU-U.S. Data Privacy Framework as set forth by the U.S. Department of Commerce.)
* Data analytics vendors, including Google Analytics ​
* To comply with applicable law or any obligations thereunder, including cooperation with law enforcement, judicial orders, and regulatory inquiries ​
* In connection with an asset sale, merger, bankruptcy, or other business transaction ​
* To enforce any applicable terms of service ​
* To ensure the safety and security of the Company and/or its users ​
* With any parent companies, subsidiaries, joint ventures, or other companies under common control with us, in which case we will require such entities to honor this Privacy Policy
* In connection with or during negotiation of any merger, financing, acquisition, or dissolution transaction or proceeding involving sale, transfer, divestiture, or disclosure of all or a portion of our business or assets. In the event of an insolvency, bankruptcy, or receivership, data may also be transferred as a business asset. If another company acquires our company, business, or assets, that company will possess the data collected by us and will assume the rights and obligations regarding your data as described in this Privacy Policy.
* When you request us to share certain information with third parties, such as through your use of login integrations ​
* With professional advisors, such as auditors, law firms, accounting firms, or KYC service providers ​
* With related companies, e.g. Ethena BVI Limited, to provide the Services

## LEGAL BASIS UNDER GDPR

The legal bases for the processing of personal data of natural persons in the European Economic Area (EEA) are detailled in the General data Protection Regulation (GDPR). The legal bases for processing your personal data are:

* In the case of the initiation of a contract or an ongoing contractual relationship (in particular for the purpose of the fulfillment of Your contract with Ethena GmbH), the legal basis follows from Art. 6 (1) lit. b GDPR;
* We are obliged by law to process Your data, e.g. by Financial Regulations (such as MiCAR Markets in Crypto Assets Regulation), Anti Money Laundering Laws, Tax Laws etc; the legal basis for such processing is Art. 6 (1) lit. c GDPR;
* Our legitimate interests under Art. 6 (1) lit. f GDPR; our legitimate interests are e.g. to safeguard the security and stability of our Services; to monitor the use of our Services in order to comply with all applicable laws; to detect, prevent, and address fraud, violations of our terms or policies, and/or other harmful or unlawful activity; to improve our Services; and for certain limited promotional purposes.
* If You have given Your consent to process Your data, the legal basis is Art. 6 (1) lit. a GDPR.

## COOKIES AND OTHER TRACKING TECHNOLOGIES

Do Not Track Signals: ​ Your browser settings may allow you to transmit a "Do Not Track" signal when you visit various websites. Like many websites, our website is not designed to respond to "Do Not Track" signals received from browsers. To learn more about "Do Not Track" signals, you can visit http://www.allaboutdnt.com/. ​ 

Cookies and Other Tracking Technologies: ​ Most browsers accept cookies automatically, but you may be able to control the way in which your devices permit the use of cookies, web beacons/clear gifs, other geolocation tracking technologies. If you so choose, you may block or delete our cookies from your browser; however, blocking or deleting cookies may cause some of the Services, including any portal features and general functionality, to work incorrectly. If you have questions regarding the specific information about you that we process or retain, as well as your choices regarding our collection and use practices, please contact us using the information listed below. ​ You can opt out of tracking by Google Analytics. ​ Your browser settings may allow you to transmit a "Do Not Track" signal when you visit various websites. Like many websites, our website is not designed to respond to "Do Not Track" signals received from browsers. To learn more about "Do Not Track" signals, you can visit http://www.allaboutdnt.com/. ​

The legal bases for the setting of cookies are legitimate interests under Art. 6 para. 1 letter f) GDPR and, if applicable, Your consent in accordance with Art. 6 (1) (b) GDPR. In the case of the initiation of a contract or an ongoing contractual relationship, the legal basis also follows from Art. 6 para. 1 sentence 1 letter b) GDPR.

## SOCIAL NETWORKS AND OTHER THIRD PARTY WEBSITES AND LINKS

We may provide links to websites or other online platforms operated by third parties, including third-party social networking platforms, such as Twitter, Discord, Telegram or Medium as well as Curve Finance & Uniswap, operated by third parties (such platforms are "Social Networks" or “Decentralized Finance Applications”). If you follow links to sites not affiliated or controlled by us, you should review their privacy and security policies and other terms and conditions. We do not guarantee and are not responsible for the privacy or security of these sites, including the accuracy, completeness, or reliability of information found on these sites. Information you provide on public or semi-public venues, including information you share or post on Social Networks, may also be accessible or viewable by other users of the Services and/or users of those third-party online platforms without limitation as to its use by us or by a third party. Our inclusion of such links does not, by itself, imply any endorsement of the content on such platforms or of their owners or operators, except as disclosed on the Services. ​

## THIRD PARTY WALLET EXTENSIONS

​Certain transactions conducted via our Services, will require you to connect a Wallet to the Services. By using such Wallet to conduct such transactions via the Services, you agree that your interactions with such third party Wallets are governed by the privacy policy for the applicable Wallet. We expressly disclaim any and all liability for actions arising from your use of third party Wallets, including but without limitation, to actions relating to the use and/or disclosure of personal information by such third party Wallets.

## PUBLIC INFORMATION OBSERVED FROM BLOCKCHAINS

We collect data from activity that is publicly visible and/or accessible on blockchains. This may include blockchain addresses and information regarding holdings, purchases, sales, or transfers of tokens, which may then be associated with other data you have provided to us.

## CHILDREN'S PRIVACY

Children under the age of 18 are not permitted to use the Services, and we do not seek or knowingly collect any personal information about children under 13 years of age. If we become aware that we have unknowingly collected information about a child under 13 years of age, we will make commercially reasonable efforts to delete such information from our database. ​ If you are the parent or guardian of a child under 13 years of age who has provided us with their personal information, you may contact us using the below information to request that it be deleted. ​

## DATA ACCESS AND CONTROL

You can view, access, edit, or delete your data for certain aspects of the Service via your Settings page. You may also have certain additional rights:

* If you are a user in the European Economic Area, you have certain rights under the European General Data Protection Regulation (“GDPR”). These include the right to
* + (i) request access and obtain a copy of your personal data;
	+ (ii) request rectification or erasure;
	+ (iii) object to or restrict the processing of your personal data; and
	+ (iv) request portability of your personal data. Additionally, if we have collected and processed your personal data with your consent, you have the right to withdraw your consent at any time.

If you wish to exercise your rights under the GDPR, CCPA, or other applicable data protection or privacy laws, please contact us at the address provided herein, specify your request, and reference the applicable law. We may ask you to verify your identity, or ask for more information about your request. We will consider and act upon any above request in accordance with applicable law. We will not discriminate against you for exercising any of these rights.

Notwithstanding the above, we cannot edit or delete any information that is stored on a blockchain, for example the Ethereum blockchain, as we do not have custody or control over any blockchains.

## DATA RETENTION

We may retain your data as long as you continue to use the Services, have an account with us, or for as long as is necessary to fulfill the purposes outlined in this Privacy Policy. We may continue to retain your data even after you deactivate your account and/or cease to use the Service if such retention is reasonably necessary to comply with our legal obligations, to resolve disputes, prevent fraud and abuse, enforce our Terms or other agreements, and/or protect our legitimate interests. Where your data is no longer required for these purposes, we will delete it.

## DATA SECURITY

We use appropriate technical and organizational measures to prevent accidental or intentional manipulation, partial or total loss, destruction or unauthorized access to your data by third parties. Our security measures are continuously improved in line with technological developments. Furthermore, all service providers commissioned by us are obliged by means of appropriate contractual agreements to take appropriate measures in accordance with the current state of the art to prevent the aforementioned risks.

Please be aware that, despite our reasonable efforts to protect your information, no security measures are perfect or impenetrable, and we cannot guarantee "perfect security." Please further note that any information you send to us electronically, while using the Services or otherwise interacting with us, may not be secure while in transit. We recommend that you do not use unsecure channels to communicate sensitive or confidential information to us. ​You are responsible for the security of your digital wallet(s), and urge you to take steps to ensure it is and remains secure.

In the event that any information under our custody and control is compromised as a result of a breach of security, we will take steps to investigate and remediate the situation and, in accordance with applicable laws and regulations, notify those individuals whose information may have been compromised.

## Rights of Data Subjects under GDPR

This section applies to you if you are able to avail yourself of certain rights under GDPR.

a) Right to information, rectification, deletion as well as rights to restriction of processing or transfer of your data to another body

You have the right to request information (Art. 15 GDPR) about your personal data and related information. In addition, you can request the correction (Art. 16 GDPR) and the deletion (Art. 17 para. 1 GDPR) of your personal data. You can also request that the processing of your personal data be restricted (Art. 18 GDPR). Furthermore, you have the right to receive your personal data from the responsible body or to have it transmitted to another responsible body (Art. 20 GDPR).

b) Revocation of consent to data processing

You can revoke your consent in accordance with Art. 6 (1) sentence 1 (a) GDPR at any time with immediate effect in accordance with Art. 7 (3) sentence 1 GDPR. Please note that data processing that took place before the revocation is not affected by the revocation and is therefore lawful despite the revocation. If you would like to make use of your right of objection, a simple notification to the person listed under no. 1.

c) Objection to profiling and direct marketing

In certain cases, you also have the right to object (Art. 21 GDPR) to the data processing.

In particular, you have the right to object at any time to the processing of your data (in particular in the case of so-called profiling) based on Art. 6 (1) sentence 1 (f) GDPR (data processing on the basis of a balancing of interests) or Art. 6 (1) sentence 1 (i) GDPR (data processing in the public interest) in accordance with Art. 21 (1) GDPR. We will then no longer process your personal data for these purposes, unless we can demonstrate compelling legitimate grounds for the processing which override the interests, rights and freedoms of the data subject, or the processing serves to establish, exercise or defend legal claims.

If your personal data is processed for direct marketing, you can also object to the processing of your data for the purpose of direct marketing at any time in accordance with Art. 21 para. 2 GDPR, including profiling, insofar as it is related to such direct marketing. If you object, your personal data will no longer be used for these direct marketing purposes.

d) Right to lodge a complaint with the competent data protection supervisory authority

If you believe that we have not complied with data protection regulations when processing your data, you can submit a complaint to the supervisory authority responsible for us. The indication of the supervisory authority is not a mandatory part of the privacy policy.

The competent data protection authority is: 

Der Hessische Beauftragte für Datenschutz und Informationsfreiheit
Prof. Dr. Alexander Roßnagel
Gustav-Stresemann-Ring 1
65189 Wiesbaden
Telefon: 0611-1408 0

## HOW TO CONTACT US

.

Last updated 4 months ago

Was this helpful?

---


# Terms of Service

Source: https://docs.ethena.fi/resources/terms-of-service

Last Revised January 2025

These Terms of Service (these “Terms”) explain the terms and conditions by which you may access and use our website, www.ethena.fi (the “Website”), operated by or on behalf of Ethena (BVI) Limited (inclusive with its affiliates, the “Company”, “we” or “us”), our App (as defined below), and any other Services provided by the Company, including any related content, tools, documentation, features and functionality collectively the “Services”.

These Terms govern your access to and use of the Services. Please read these Terms carefully, as they include important information about your legal rights. By accessing and/or using the Services, you are agreeing to these Terms. If you do not understand or agree to these Terms, please do not use the Services.

For purposes of these Terms, “you” and “your” means you as the user of the Services. If you use the Services on behalf of a company or other entity then “you” includes you and that entity, and you represent and warrant that (a) you are an authorized representative of the entity with the authority to bind the entity to these Terms, and (b) you agree to these Terms on the entity's behalf.

As of 29 July 2024 Ethena GmbH, a wholly-owned subsidiary of Ethena Labs, S.A., and affiliate of the Company, submitted an application for authorization to make an offer to the public of an asset-referenced token pursuant to Art. 16 et seq. of Regulation (EU) 2023/1114 ("MiCAR") with Bundesanstalt für Finanzdienstleistungsaufsicht (“BaFin”) with respect to USDe. BaFin has significant experience and expertise with respect to crypto assets and we look forward to a collaborative process. As the application was submitted prior to the 30 July 2024 deadline. According to MiCAR,grandfathering provisions apply on this basis (see Art. 143 para. 4 MiCAR) which allow Ethena GmbH to issue USDe during the authorization process. Updates will be provided publicly as appropriate as the authorization process proceeds. Please refer to the relevant USDe Terms and Conditions located at https://docs.ethena.fi.

The Company and Ethena BVI are dual issuers of USDe. For terms applicable to relevant users, please refer to the relevant USDe Terms and Conditions.

1. The Services

1.1 Services. The Services provide an interface (the “App”) that displays data for the purpose of enabling users to interface, via a third-party wallet application (e.g., Metamask), with certain components of a set of open-sourced smart contracts deployed on decentralized blockchains, namely the “staking” mechanism inherent to the Ethena Protocol. The set of smart contracts maintained and operated by the Ethena Foundation and its affiliates, collectively with off-chain infrastructure (e.g., off-exchange custody solutions and exchange relationships) maintained and operated by Ethena GmbH and its affiliates, are referred to herein as the “Protocol”. In addition, the App displays data for the purpose of enabling users to interface, via a third-party wallet application, with certain components of open-sourced smart contract systems deployed on decentralized blockchains, such as certain liquidity pools on Curve Finance and Uniswap (the “Third Party Protocols”).

Documentation relevant to the Services, the App, and the Protocol are available at docs.ethena.fi (the “Documentation”). The Protocol itself is not part of the Services, and your use of the Protocol is entirely at your own risk. Additionally, the third party technologies required to be used or interacted with in order to interact with the Protocol, including but not limited to a Wallet (as defined below, and collectively the “Third-Party Tools”), are not part of the Services, and your use of such Third-Party Tools are entirely at your own risk. The App is separate and distinct from the Protocol and any Third-Party Tools and is not essential for the purpose of accessing or otherwise interacting with the Protocol. The App merely displays blockchain data and provides a web application that reduces the complexity of using the Third-Party Tools to otherwise interact with the Protocol. Activity on the Protocol is conducted via permissionless smart contracts as well as certain aspects of off-chain infrastructure detailed in the Documentation and maintained by the Ethena Foundation and its affiliates, and users or other developers are free to create their own interfaces to interact with the Protocol.

When you utilize any data inputs provided by the App to execute transactions, you are interacting with public blockchains, which provide transparency into your transactions. The Company does not control and is not responsible for any information you make public on any public blockchain by taking actions utilizing data provided by the App or the Services.

Distributions of ENA Tokens, including but not limited to airdrops or other rewards programs displayed on the App (including, but not limited, to, smart contracts within which certain tokens may be locked, and the maintenance of rewards balances), are managed by Ethena OpCo Ltd., a wholly-owned subsidiary of the Ethena Foundation, and other independent third parties. The Company does not offer, manage, or distribute ENA Tokens and do not assume any responsibility for such programs. The App merely displays relevant data provided by Ethena OpCo Ltd. or third parties. You acknowledge and agree that such programs are separate from the Services and the Company expressly disclaims any warranties or liability related to the ENA Tokens, their distribution, or associated rewards programs.

The sUSDe staking smart contract, including the management and transfer of USDe rewards, is maintained by Ethena OpCo Ltd. The App displays relevant data provided by Ethena OpCo Ltd. pertaining to sUSDe, including any references to APY. 

Any communications, whether via the App or other media, by Ethena Labs and its affiliates relating to sUSDe and ENA are done as a service provider to the Ethena Foundation and Ethena OpCo Ltd. 

1.2 Wallets. To use certain of the Services it may be necessary to connect a third-party digital wallet (“Wallet”) to the App. In such cases, by using a Wallet in connection with the Services, you agree that you are using the Wallet under the terms and conditions of the applicable third-party provider of such Wallet. Wallets are not associated with, maintained by, supported by or affiliated with the Company. You acknowledge and agree that we are not party to any transactions concluded while or after accessing our App, and we do not have possession, custody or control over any digital assets appearing on the App. When you interact with the App, you retain control over your digital assets at all times. The Company accepts no responsibility or liability to you in connection with your use of a Wallet or data provided by the App in consummating transactions using a Wallet, and makes no representations and warranties regarding how the Services will interact with any specific Wallet. The private keys and/or seed phrases necessary to access the assets held in a Wallet are not held by or known to the Company. The Company has no ability to help you access or recover your private keys and/or seed phrases for your Wallet, so please keep them in a safe place.

1.3 Updates; Monitoring. We may make any improvements, modifications or updates to the Services, including but not limited to changes and updates to the underlying software, infrastructure, security protocols, documentation, technical configurations or service features (the “Updates”) from time to time. Your continued access to and use of the Services are subject to such Updates and you shall accept any patches, system upgrades, bug fixes, feature modifications, or other maintenance work that arise out of such Updates. We are not liable for any failure by you to accept and use such Updates in the manner specified or required by us. Although the Company is not obligated to monitor access to or participation in the Services, it has the right to do so for the purpose of operating the Services, to ensure compliance with the Terms and to comply with applicable law or other legal requirements.

1.4 Fees. While the Company does not presently charge any fees for the Services or the App, transactions executed by you utilizing data provided by the App and your use of the Services may cause you to incur fees such as blockchain gas or similar network fees, as well as fees charged by the Protocol, if any, and Third Party Protocols. All such fees displayed within your Wallet utilizing data inputs provided by the App are merely estimates and may not reflect actual costs incurred in broadcasting a transaction for execution according to the applicable consensus mechanism. Additionally, your external Wallet provider may impose a fee. We are not responsible for any fees charged by a third party. Due to the nature of distributed, public blockchains, transactions executed by you utilizing data provided by the App and the Services are non-refundable and the Company is not able to alter or mitigate any such fees. You will be responsible for paying any and all taxes, duties and assessments now or hereafter claimed or imposed by any governmental authority associated with your use of the Services, the App, the Protocol, and Third-Party Protocols. In certain cases, your transactions may not be successful due to an error with the blockchain or the Wallet, or due to changes in the distributed blockchain environment (e.g., during a spike in demand for block space and/or activity on the relevant network). We accept no responsibility or liability to you for any such failed transactions, or any transaction or gas fees that may be incurred by you in connection with such failed transactions.

2. Who May Use the Services. You must be 18 years of age or older and not be a Prohibited Person to use the Services. A “Prohibited Person” is any person or entity that is (a) listed on (i) any U.S. Government list of prohibited or restricted parties, including the U.S. Treasury Department's list of Specially Designated Nationals or the U.S. Department of Commerce Denied Persons List or Entity List; (ii) the EU consolidated list of persons, groups and entities subject to financial sanctions; (iii) the UK Consolidated List of Financial Sanctions Targets; or (iv) any of Switzerland's respective sanctions lists, (b) located or organized in any U.S. embargoed countries or any country that has been designated by the U.S. Government as “terrorist supporting”, (c) a citizen, resident, or organized in, the following jurisdictions (the “Prohibited Jurisdictions”): Abkhazia, Afghanistan, Angola, Belarus, Burundi, Central African Republic, Congo, Cuba, Crimea, Ethiopia, Guinea-Bissau, Iran, Ivory Coast (Cote D’Ivoire), Lebanon, Liberia, Libya, Mali, Burma (Myanmar), Nicaragua, North Korea, Northern Cyprus, Russia, Somalia, Somaliland, South Ossetia, South Sudan, Sudan, Syria, Ukraine (Donetsk and Luhansk regions), United States, Venezuela, Yemen, Zimbabwe; (d) otherwise a party with which the Company is prohibited to deal under the laws of the U.S., the EU (or any of its Member States), the UK, or any applicable foreign jurisdiction, or (e) owned or controlled by such persons or entities listed in (a)-(d). The Company may utilize certain tools, such as IP-based geofencing, to enforce the above restrictions. By using the Services and/or the App, you represent that you are not a Prohibited Person.

You acknowledge and agree that you are solely responsible for complying with all applicable laws of the jurisdiction you are located or accessing the Services from in connection with your use of the Services. By using the Services, you represent and warrant that you meet these requirements and will not be using the Services for any illegal activity or to engage in the prohibited activities in Section 5.3. We may require you to provide additional information and documents regarding your use of the Services, including in case of application of any applicable law or regulation, including laws related to anti-money laundering or for countering the financing of terrorism, or the request of any competent authority. We may also require you to provide additional information or documents in cases where we have reason to believe: (i) that your Wallet is being used for illegal money laundering or for any other illegal activity; or (ii) you have concealed or reported false identification information or other details.

3. Location of Our Privacy Policy Our Privacy Policy describes how we handle the information you provide to us when you use the Services. For an explanation of our privacy practices, please visit our Privacy Policy located at https://docs.ethena.fi/resources/privacy-policy.

4. Rights We Grant You

4.1 Right to Use Services. We hereby permit you to use the Services for your personal non-commercial use only, provided that you comply with these Terms in connection with all such use. If any software, content or other materials owned or controlled by us are distributed to you as part of your use of the Services, we hereby grant you, a personal, non-assignable, non-sublicensable, non-transferrable, and non-exclusive right and license to access and display such software, content, and materials provided to you as part of the Services, in each case for the sole purpose of enabling you to use the Services as permitted by these Terms. Your access and use of the Services may be interrupted from time to time for any of several reasons, including, without limitation, the malfunction of equipment, periodic updating, maintenance or repair of the Service or other actions that Company, in its sole discretion, may elect to take.

4.2 Restrictions On Your Use of the Services. You may not do any of the following in connection with your use of the Services, unless applicable laws or regulations prohibit these restrictions or you have our written permission to do so: (a) download, modify, copy, distribute, transmit, display, perform, reproduce, duplicate, publish, license, create derivative works from, or offer for sale any information contained on, or obtained from or through, the Services, except for temporary files that are automatically cached by your web browser for display purposes, or as otherwise expressly permitted in these Terms; (b) duplicate, decompile, reverse engineer, disassemble or decode the Services (including any underlying idea or algorithm), or attempt to do any of the same; (c) use, reproduce or remove any copyright, trademark, service mark, trade name, slogan, logo, image, or other proprietary notation displayed on or through the Services; (d) use automation software (bots), hacks, modifications (mods) or any other unauthorized third-party software designed to modify the Services; (e) exploit the Services for any commercial purpose, including without limitation communicating or facilitating any commercial advertisement or solicitation; (f) access or use the Services in any manner that could disable, overburden, damage, disrupt or impair the Services or interfere with any other party's access to or use of the Services or use any device, software or routine that causes the same; (g) attempt to gain unauthorized access to, interfere with, damage or disrupt the Services or the computer systems, wallets, accounts, protocols or networks connected to the Services; (h) circumvent, remove, alter, deactivate, degrade or thwart any technological measure or content protections of the Services or the computer systems, wallets, accounts, protocols or networks connected to the Services; (i) use any robot, spider, crawler or other automatic device, process, software or query that intercepts, “mines,” scrapes, or otherwise accesses the Services to monitor, extract, copy, or collect information or data from or through the Services, or engage in any manual process to do the same; (j) introduce any viruses, trojan horses, worms, logic bombs or other materials that are malicious or technologically harmful into our systems; (k) submit, transmit, display, perform, post or store any content that is inaccurate, unlawful, defamatory, obscene, lewd, lascivious, filthy, excessively violent, pornographic, invasive of privacy or publicity rights, harassing, threatening, abusive, inflammatory, harmful, hateful, cruel or insensitive, deceptive, or otherwise objectionable, use the Services for illegal, harassing, bullying, unethical or disruptive purposes, or otherwise use the Services in a manner that is obscene, lewd, lascivious, filthy, excessively violent, harassing, harmful, hateful, cruel or insensitive, deceptive, threatening, abusive, inflammatory, pornographic, inciting, organizing, promoting or facilitating violence or criminal or harmful activities, defamatory, obscene or otherwise objectionable; (l) violate any applicable law or regulation in connection with your access to or use of the Services; or (m) access or use the Services in any way not expressly permitted by these Terms.

4.3 Interactions with Other Users on the Services. You are responsible for your interactions with other users on or through the Services. While we reserve the right to monitor interactions between users, we are not obligated to do so, and we cannot be held liable for your interactions with other users, or for any user's actions or inactions. If you have a dispute with one or more users, you release us (and our affiliates and subsidiaries, and our and their respective officers, directors, employees and agents) from claims, demands and damages (actual and consequential) of every kind and nature, known and unknown, arising out of or in any way connected with such disputes. In entering into this release you expressly waive any protections (whether statutory or otherwise) that would otherwise limit the coverage of this release to include only those claims which you may know or suspect to exist in your favor at the time of agreeing to this release.

5. Ownership and Content

5.1 Ownership of the Services. The Services, including their “look and feel” (e.g., text, graphics, images, logos), proprietary content, information and other materials, are protected under copyright, trademark and other intellectual property laws. You agree that the Company and/or its licensors own all right, title and interest in and to the Services (including any and all intellectual property rights therein) and you agree not to take any action(s) inconsistent with such ownership interests. We and our licensors reserve all rights in connection with the Services and its content, including, without limitation, the exclusive right to create derivative works.

5.2 Ownership of Trademarks. The Company's name, trademarks and logos and all related names, logos, product and service names, designs and slogans are trademarks of the Company or its affiliates or licensors. Other names, logos, product and service names, designs and slogans that appear on the Services are the property of their respective owners, who may or may not be affiliated with, connected to, or sponsored by us.

5.3 Ownership of Feedback. We welcome feedback, bug reports, comments and suggestions for improvements to the Services (“Feedback”). You acknowledge and expressly agree that any contribution of Feedback does not and will not give or grant you any right, title or interest in the Services or in any such Feedback. All Feedback becomes the sole and exclusive property of the Company, and the Company may use and disclose Feedback in any manner and for any purpose whatsoever without further notice or compensation to you and without retention by you of any proprietary or other right or claim. You hereby assign to the Company any and all right, title and interest (including, but not limited to, any patent, copyright, trade secret, trademark, show-how, know-how, moral rights and any and all other intellectual property right) that you may have in and to any and all Feedback.

6. Third Party Services and Materials. The Services, through the App, may provide data relevant to the Third-Party Protocols. The Services may display, include or make available content, data, information, applications or materials from third parties (“Third-Party Materials”) or provide links to certain third party websites. The Company does not endorse any Third-Party Materials or the use of any provider of any Third-Party Protocols. You agree that your access and use of such Third-Party Protocols and Third-Party Materials is governed solely by the terms and conditions of such Third-Party Protocols and Third-Party Materials, as applicable. The Company is not responsible or liable for, and make no representations as to any aspect of such Third-Party Materials and Third-Party Protocols, including, without limitation, their content, operation, or the manner in which they handle, protect, manage or process data or any interaction between you and the provider of such Third-Party Protocols. The Company is not responsible for examining or evaluating the content, accuracy, completeness, availability, timeliness, validity, copyright compliance, legality, decency, quality, risk, functionality, safety, or any other aspect of such Third Party Protocols or Third Party Materials or websites. You irrevocably waive any claim against the Company with respect to such Third-Party Protocols and Third-Party Materials. We are not liable for any damage or loss caused or alleged to be caused by or in connection with your enablement, access or use of any such Third-Party Protocols or Third-Party Materials, or your reliance on the privacy practices, data security processes or other policies of such Third-Party Protocols. Third-Party Protocols, Third-Party Materials and links to other websites are provided solely as a convenience to you.

7. Disclaimers, Limitations of Liability and Indemnification

7.1 Disclaimers. Your access to and use of the Services and the Protocol are at your own risk. You understand and agree that the Services are provided to you on an “AS IS” and “AS AVAILABLE” basis. Without limiting the foregoing, to the maximum extent permitted under applicable law, the Company, its parents, affiliates, related companies, officers, directors, employees, agents, representatives, partners and licensors (the “Company Entities”), and Multisig Members (as defined below) DISCLAIM ALL WARRANTIES AND CONDITIONS, WHETHER EXPRESS, IMPLIED OR STATUTORY, INCLUDING WITHOUT LIMITATION ANY WARRANTIES RELATING TO TITLE, MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, NON-INFRINGEMENT, USAGE, QUALITY, PERFORMANCE, SUITABILITY OR FITNESS OF THE SERVICES AND THE PROTOCOL FOR ANY PARTICULAR PURPOSE, OR AS TO THE ACCURACY, QUALITY, SEQUENCE, RELIABILITY, WORKMANSHIP OR TECHNICAL CODING THEREOF, OR THE ABSENCE OF ANY DEFECTS THEREIN WHETHER LATENT OR PATENT. The Company Entities and MultiSig Members make no warranty or representation and disclaim all responsibility and liability for: (a) the completeness, accuracy, availability, timeliness, security or reliability of the Services and the Protocol; (b) any harm to your computer system, loss of data, or other harm that results from your access to or use of the Services or the Protocol; (c) the operation or compatibility with any other application or any particular system or device, including any Wallets; and (d) whether the Services or the Protocol will meet your requirements or be available on an uninterrupted, secure or error-free basis.

The Company's affiliate in Italy, Ethena Italia S.r.l., holds a VASP registration with the Italian Organismo Agente E Mediatori as a service provider. In addition, as noted above, the Company’s affiliate in Germany, Ethena GmbH, submitted an application for authorization to make an offer to the public of an asset-referenced token pursuant to MiCAR with BaFin with respect to USDe. Aside from this registration, the Company and its affiliates are not registered in any capacity with any other regulatory body in any jurisdiction. You understand and acknowledge that we do not broker trading orders on your behalf, match orders for buyers and sellers of securities or any other assets, or offer any products, financial or otherwise, for sale or distribution. We also do not facilitate the execution or settlement of your transactions, which occur entirely on public distributed blockchains. The App is strictly a means by which users may construct transaction data to be utilized by the individual user by executing transactions utilizing Wallets.

No advice or information, whether oral or written, obtained from the Company Entities or through the Services, will create any warranty or representation not expressly made herein. You agree and understand that all transfers, staking, or other actions you perform utilizing transaction data provided by the App are considered unsolicited, which means that you have not received any investment advice from us in connection with any such action, we have not actively solicited your use of the Services, and that we do not conduct a suitability review of any such action.

All information provided by the App and our Services is for informational purposes only and should not be construed as investment advice. You should not take, or refrain from taking, any action based on any information contained in the App or obtained via the Services. We do not make any investment recommendations to you or opine on the merits of any investment transaction or opportunity. You alone are responsible for determining whether any investment, investment strategy or related transaction is appropriate for you based on your personal investment objectives, financial circumstances, and risk tolerance.

7.2 Limitations of Liability. TO THE EXTENT NOT PROHIBITED BY LAW, YOU AGREE THAT IN NO EVENT WILL THE COMPANY ENTITIES OR MULTISIG MEMBERS BE LIABLE (A) FOR DAMAGES OF ANY KIND, INCLUDING DIRECT, INDIRECT, SPECIAL, EXEMPLARY, INCIDENTAL, CONSEQUENTIAL OR PUNITIVE DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES, LOSS OF USE, DATA OR PROFITS, BUSINESS INTERRUPTION OR ANY OTHER DAMAGES OR LOSSES, ARISING OUT OF OR RELATED TO YOUR USE OR INABILITY TO USE THE SERVICES), HOWEVER CAUSED AND UNDER ANY THEORY OF LIABILITY, WHETHER UNDER THESE TERMS OR OTHERWISE ARISING IN ANY WAY IN CONNECTION WITH THE SERVICES OR THESE TERMS AND WHETHER IN CONTRACT, STRICT LIABILITY OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) EVEN IF THE COMPANY ENTITIES HAVE BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE, OR (B) FOR ANY OTHER CLAIM, DEMAND OR DAMAGES WHATSOEVER RESULTING FROM OR ARISING OUT OF OR IN CONNECTION WITH THESE TERMS OR THE DELIVERY, USE OR PERFORMANCE OF THE SERVICES. THE COMPANY ENTITIES' TOTAL LIABILITY TO YOU FOR ANY DAMAGES FINALLY AWARDED SHALL NOT EXCEED ONE HUNDRED DOLLARS ($100.00). SOME JURISDICTIONS (SUCH AS THE STATE OF NEW JERSEY) DO NOT ALLOW THE EXCLUSION OR LIMITATION OF INCIDENTAL OR CONSEQUENTIAL DAMAGES, SO THE ABOVE EXCLUSION OR LIMITATION MAY NOT APPLY TO YOU.

7.3 Assumption of Risks.

(a) By using the Services, you represent that you have sufficient knowledge and experience in business and financial matters, including a sufficient understanding of blockchain technologies, cryptocurrencies and other digital assets, storage mechanisms (such as Wallets), and blockchain-based software systems to be able to assess and evaluate the risks and benefits of the Services contemplated hereunder, and will bear the risks thereof, including loss of all amounts paid, and the risk that the cryptocurrencies and other digital assets may have little or no value. You acknowledge and agree that there are risks associated with purchasing and holding cryptocurrency, using blockchain technology and staking cryptocurrency. These include, but are not limited to, risk of losing access to cryptocurrency due to slashing, loss of private key(s), custodial error or purchaser error, risk of mining or blockchain attacks, risk of hacking and security weaknesses, risk of unfavorable regulatory intervention in one or more jurisdictions, risk related to token taxation, risk of personal information disclosure, risk of uninsured losses, volatility risks, and unanticipated risks. You acknowledge that cryptocurrencies and other similar digital assets are neither (i) deposits of or guaranteed by a bank nor (ii) insured by the FDIC or by any other governmental agency.

(b) There are certain multi-signature crypto wallets (the “MultiSigs”, and the signatories to such MultiSigs, the “MultiSig Members”) that have certain controls related to the Protocol, that may include, but are not limited to, the ability to pause certain functionality of the Protocol, implement, or influence upgrades to the Protocol (or any aspect thereof) and certain other controls of the functionality of the Protocol as described in the Documentation or in public communications. While the MultiSigs may have MultiSig Members that are employed or engaged by the Company, they may be controlled partially or entirely by MultiSig Members that are unaffiliated third parties over which we have no or limited control. We will not be able to control the actions of such MultiSig Members if they are not employed or engaged by us and thus certain MultiSigs will be outside of our control. The Company therefore cannot be held liable for any action, or inaction, relating to such a MultiSig.

(c) The regulatory regimes governing blockchain technologies, cryptocurrencies and other digital assets are uncertain, and new regulations or policies may materially adversely affect the potential utility or value of the Services, the Protocol, Third-Party Protocols, cryptocurrencies and other digital assets, or the ability of the Company to continue to provide or support such Services and/or the App. Additionally, taxation of activities and transactions in cryptocurrencies and other digital assets is uncertain in certain cases in certain jurisdictions. You are encouraged to consult with your own tax advisor with respect to potential tax implications associated with utilizing the Services, the App, and the Protocol.

(d) We cannot control or influence market sentiment or liquidity or how third-party services or platforms support, quote, restrict or provide access to, or value cryptocurrencies and other digital assets and we expressly deny and disclaim any liability to you and deny any obligations to indemnify or hold you harmless for any losses you may incur as a result of fluctuations in the value of cryptocurrencies or other digital assets.

(e) Smart contracts execute automatically when certain conditions are met. Transactions on blockchains or using smart contracts often cannot be stopped or reversed, so vulnerabilities in the programming, design, or implementation of a blockchain, the Protocol, any deployed smart contracts, or a Third-Party Protocol may arise due to hacking or other security incidents and could result in significant adverse effects, including but not limited to, significant volatility or loss of any digital assets elected into the Protocol.

(f) The Documentation describes certain risks associated with the Protocol in detail. Please review the Documentation for additional risks associated with utilizing the Services or the App in conjunction with your use of, and access to, the Protocol. The Company hereby disclaims any and all liability associated with risks disclosed in the Documentation to the fullest extent provided by applicable law.

7.4 Indemnification. By entering into these Terms and accessing or using the Services, you agree that you shall defend, indemnify and hold the Company Entities and MultiSig Members harmless from and against any and all claims, costs, damages, losses, liabilities and expenses (including attorneys' fees and costs) incurred by the Company Entities arising out of or in connection with: (a) your violation or breach of any term of these Terms or any applicable law or regulation; (b) your violation of any rights of any third party; (c) your misuse of the Services; or (d) your negligence or willful misconduct. If you are obligated to indemnify any Company Entity hereunder, then you agree that Company (or, at its discretion, the applicable Company Entity) will have the right, in its sole discretion, to control any action or proceeding and to determine whether Company wishes to settle, and if so, on what terms, and you agree to fully cooperate with Company in the defense or settlement of such claim.

7.5 Third Party Beneficiaries. You and the Company acknowledge and agree that the Company Entities (other than the Company) and the MultiSig Members are third party beneficiaries of these Terms, including under Section 7 and 8.

8. ARBITRATION AND CLASS ACTION WAIVER

8.1 PLEASE READ THIS SECTION CAREFULLY – IT MAY SIGNIFICANTLY AFFECT YOUR LEGAL RIGHTS, INCLUDING YOUR RIGHT TO FILE A LAWSUIT IN COURT AND TO HAVE A JURY HEAR YOUR CLAIMS. IT CONTAINS PROCEDURES FOR MANDATORY BINDING ARBITRATION AND A CLASS ACTION WAIVER.

8.2 Informal Process First. You and the Company agree that in the event of any dispute between you and the Company Entities or the MultiSig Members, either party will first contact the other party and make a good faith sustained effort to resolve the dispute before resorting to more formal means of resolution, including without limitation, any court action, after first allowing the receiving party 30 days in which to respond. Both you and the Company agree that this dispute resolution procedure is a condition precedent which must be satisfied before initiating any arbitration against you, any Company Entity or any MultiSig Members, as applicable.

8.3 Arbitration Agreement and Class Action Waiver. After the informal dispute resolution process, any remaining dispute, controversy, or claim (collectively, “Claim”) relating in any way to the Services, including the App, any use or access or lack of access thereto, and any other usage of the Protocol even if interacted with outside of the Services or App, will be resolved by arbitration, including threshold questions of arbitrability of the Claim. You and the Company agree that any Claim including those not of a contractual nature - arising out of, related or connected to the Services, the App, or otherwise, shall be settled by arbitration under the Rules of the Milan Chamber of Arbitration (the Rules), by three arbitrators, appointed in accordance with the Rules, which are deemed to be incorporated by reference into this clause. The language of arbitration will be English. Any arbitration under these Terms will take place on an individual basis – class arbitrations and class actions are not permitted. You understand that by agreeing to these Terms, you and the Company are each waiving the right to trial by jury or to participate in a class action or class arbitration.

European Online Dispute Resolution Platform and Consumer Arbitration:

Among https://ec.europa.eu/consumers/odr/, the European Commission has set up a European Online Dispute Resolution (ODR) platform. Ethena is neither willing nor obliged to participate in the online dispute resolution procedure within the framework of the ODR platform. Furthermore, Ethena is not willing and not obliged to participate in dispute resolution proceedings before a consumer arbitration board.

8.4 Exceptions. Notwithstanding the foregoing, you and the Company agree that the following types of disputes will be resolved in a court of proper jurisdiction: (i) disputes or claims within the jurisdiction of a small claims court consistent with the jurisdictional and dollar limits that may apply, as long as it is brought and maintained as an individual dispute and not as a class, representative, or consolidated action or proceeding; (ii) disputes or claims where the sole form of relief sought is injunctive relief (including public injunctive relief); or (iii) intellectual property disputes.

8.5 Costs of Arbitration. Payment of all filing, administration, and arbitrator costs and expenses will be governed by the Rules, except that if you demonstrate that any such costs and expenses owed by you under those rules would be prohibitively more expensive than a court proceeding, the Company will pay the amount of any such costs and expenses that the arbitrator determines are necessary to prevent the arbitration from being prohibitively more expensive than a court proceeding (subject to possible reimbursement as set forth below). Fees and costs may be awarded as provided pursuant to applicable law. If the arbitrator finds that either the substance of your claim or the relief sought in the Claim is frivolous, then the payment of all fees will be governed by the Rules. In that case, you agree to reimburse the Company for all monies previously disbursed by it that are otherwise your obligation to pay under the applicable rules.

8.6 Opt-Out. You have the right to opt-out and not be bound by the arbitration provisions set forth in these Terms by sending written notice of your decision to opt-out to finance@ethenalabs.xyz. The notice must be sent to the Company within thirty (30) days of your first accessing the Services or agreeing to these Terms; otherwise you shall be bound to arbitrate disputes on a non-class basis in accordance with these Terms. If you opt out of only the arbitration provisions, and not also the class action waiver, the class action waiver still applies. You may not opt out of only the class action waiver and not also the arbitration provisions. If you opt-out of these arbitration provisions, the Company also will not be bound by them.

8.7 WAIVER OF RIGHT TO BRING CLASS ACTION AND REPRESENTATIVE CLAIMS. TO THE FULLEST EXTENT PERMITTED BY APPLICABLE LAW, YOU AND THE COMPANY EACH AGREE THAT ANY PROCEEDING TO RESOLVE ANY DISPUTE, CLAIM OR CONTROVERSY WILL BE BROUGHT AND CONDUCTED ONLY IN THE RESPECTIVE PARTY'S INDIVIDUAL CAPACITY AND NOT AS PART OF ANY CLASS (OR PURPORTED CLASS), CONSOLIDATED, MULTIPLE-PLAINTIFF, OR REPRESENTATIVE ACTION OR PROCEEDING (“CLASS ACTION”). YOU AND THE COMPANY AGREE TO WAIVE THE RIGHT TO PARTICIPATE AS A PLAINTIFF OR CLASS MEMBER IN ANY CLASS ACTION. YOU AND THE COMPANY EXPRESSLY WAIVE ANY ABILITY TO MAINTAIN A CLASS ACTION IN ANY FORUM. IF THE DISPUTE IS SUBJECT TO ARBITRATION, THE ARBITRATOR WILL NOT HAVE THE AUTHORITY TO COMBINE OR AGGREGATE CLAIMS, CONDUCT A CLASS ACTION, OR MAKE AN AWARD TO ANY PERSON OR ENTITY NOT A PARTY TO THE ARBITRATION. FURTHER, YOU AND THE COMPANY AGREE THAT THE ARBITRATOR MAY NOT CONSOLIDATE PROCEEDINGS FOR MORE THAN ONE PERSON'S CLAIMS, AND IT MAY NOT OTHERWISE PRESIDE OVER ANY FORM OF A CLASS ACTION. FOR THE AVOIDANCE OF DOUBT, HOWEVER, YOU CAN SEEK PUBLIC INJUNCTIVE RELIEF TO THE EXTENT AUTHORIZED BY LAW AND CONSISTENT WITH THE EXCEPTIONS CLAUSE ABOVE. IF THIS CLASS ACTION WAIVER IS LIMITED, VOIDED, OR FOUND UNENFORCEABLE, THEN, UNLESS THE PARTIES MUTUALLY AGREE OTHERWISE, THE PARTIES' AGREEMENT TO ARBITRATE SHALL BE NULL AND VOID WITH RESPECT TO SUCH PROCEEDING SO LONG AS THE PROCEEDING IS PERMITTED TO PROCEED AS A CLASS ACTION. IF A COURT DECIDES THAT THE LIMITATIONS OF THIS PARAGRAPH ARE DEEMED INVALID OR UNENFORCEABLE, ANY PUTATIVE CLASS, PRIVATE ATTORNEY GENERAL OR CONSOLIDATED OR REPRESENTATIVE ACTION MUST BE BROUGHT IN A COURT OF PROPER JURISDICTION AND NOT IN ARBITRATION.

9. Additional Provisions

9.1 Updating These Terms. We may modify these Terms from time to time in which case we will update the “Last Revised” date at the top of these Terms. If we make changes that are material, we will use reasonable efforts to attempt to notify you, such as by e-mail and/or by placing a prominent notice on the first page of the Website. However, it is your sole responsibility to review these Terms from time to time to view any such changes. The updated Terms will be effective as of the time of posting, or such later date as may be specified in the updated Terms. Your continued access or use of the Services after the modifications have become effective will be deemed your acceptance of the modified Terms. No amendment shall apply to a dispute for which an arbitration has been initiated prior to the change in Terms.

9.2 Suspension; Termination. If you breach any of the provisions of these Terms, all licenses granted by the Company will terminate automatically. Additionally, the Company may, in its sole discretion, suspend or terminate your access to or use of any of the Services, with or without notice, for any or no reason, including, without limitation, (i) if we believe, in our sole discretion, you have engaged in any of the prohibited activities set forth in Section 4.2; (ii) if you provide any incomplete, incorrect or false information to us; (iii) if you have breached any portion of these Terms; (iv) if you are a Prohibited Person and/or reside in a Prohibited Jurisdiction; and/or (v) if we determine such action is necessary to comply with these Terms, any of our policies, procedures or practices, or any law rule or regulation. All sections which by their nature should survive the termination of these Terms shall continue in full force and effect subsequent to and notwithstanding any termination of this Agreement by the Company or you. Termination will not limit any of the Company's other rights or remedies at law or in equity.

9.3 Injunctive Relief. You agree that a breach of these Terms will cause irreparable injury to the Company for which monetary damages would not be an adequate remedy and the Company shall be entitled to equitable relief in addition to any remedies it may have hereunder or at law without a bond, other security or proof of damages.

9.4 Force Majeure. We will not be liable or responsible to you, nor be deemed to have defaulted under or breached these Terms, for any failure or delay in fulfilling or performing any of our obligations under these Terms or in providing the Services, when and to the extent such failure or delay is caused by or results from any events beyond our ability to control, including acts of God; flood, fire, earthquake, epidemics, pandemics, tsunami, explosion, war, invasion, hostilities (whether war is declared or not), terrorist threats or acts, riot or other civil unrest, government order, law, or action, embargoes or blockades, strikes, labor stoppages or slowdowns or other industrial disturbances, shortage of adequate or suitable Internet connectivity, telecommunication breakdown or shortage of adequate power or electricity, and other similar events beyond our control.

9.5 Miscellaneous. If any provision of these Terms shall be unlawful, void or for any reason unenforceable, then that provision shall be deemed severable from these Terms and shall not affect the validity and enforceability of any remaining provisions. These Terms and the licenses granted hereunder may be assigned by the Company but may not be assigned by you without the prior express written consent of the Company. No waiver by either party of any breach or default hereunder shall be deemed to be a waiver of any preceding or subsequent breach or default. The section headings used herein are for reference only and shall not be read to have any legal effect. The Services are operated by us in the European Union. Those who choose to access the Services from locations outside the European Union do so at their own initiative and are responsible for compliance with applicable local laws. These Terms are governed by the laws of Germany, without regard to conflict of laws rules, and the proper venue for any disputes arising out of or relating to any of the same will be the courts in Germany.

9.6 How to Contact Us. You may contact us regarding the Services or these Terms by e-mail at finance@ethenalabs.xyz.

Last updated 4 months ago

Was this helpful?

---


# USDe Terms and Conditions - EEA

Source: https://docs.ethena.fi/resources/usde-terms-and-conditions-eea

Asset-Referenced Tokens - By Ethena GmbH

Effective January 01, 2025

INTRODUCTION

These USDe terms and conditions, together with any schedules and policies referred to in them (together, the “Terms and Conditions” and each, a “Condition”) are applicable to the USDe Tokens (the “Tokens”) issued by Ethena GmbH (the “Issuer”, “we”, “us”, “our”). These Terms and Conditions are supplemental to the Terms of Service provided at https://ethena-labs.gitbook.io/ethena-labs/resources/terms-of-service (the “Terms of Service”). Capitalized terms used in these Terms and Conditions that are not defined herein have the definitions ascribed to them in the Terms of Service.

You represent that you are at least the age of majority in your jurisdiction and have the full right, power, and authority to enter into and comply with the terms and conditions of these Terms and Conditions on behalf of yourself and any company or legal entity for which you may act. If you are entering into these Terms and Conditions on behalf of an entity, you represent to us that you have the legal authority to bind such entity.

You further represent that you are not (a) the subject of economic or trade sanctions administered or enforced by any governmental authority or otherwise designated on any list of prohibited or restricted parties or (b) a citizen, resident, or organized in a jurisdiction or territory that is the subject of comprehensive country-wide, territory-wide, or regional economic sanctions. Finally, you represent that you will fully comply with all applicable laws and regulations, and that you will not conduct, promote, or otherwise facilitate any illegal activity.

YOU AND WE AGREE AS FOLLOWS:

## 1. Interpretation

1.1. In these Terms and Conditions, the following words and expressions have the following meanings unless inconsistent with the context:

“Applicable Law(s)”

means all laws, statutes, regulatory rules, and regulations that apply to the Parties in connection with these Terms and Conditions from time to time;

 

“Blockchains”

means all blockchains on which the Issuer offers to distribute Tokens, including the Ethereum blockchain.

“Business Day”

means a day on which (i) relevant commercial banks are open, and/or (ii) banks in Frankfurt are open.

 

“Greenlisted”, “Greenlisting”

means the completion of both the onboarding as described in Condition 2 and the KYC/AML Requirements.

 

“Issuer”

means the Ethena GmbH, Kurfürstendamm 15, 10719 Berlin, Federal Republic of Germany, registered in the commercial register Berlin-Charlottenburg under the registration number HRB 264787 B;

 

“KYC/AML Requirements”

mean the know your client and anti-money laundering processes established by the Issuer to ensure compliance with Applicable Law;

 

“Party”, “Parties”

you and us as the parties to these Terms and Conditions.

 

“Token(s)”

are the digital USDe tokens distributed by the Issuer which have a smart contract that is implemented on the Blockchains.

 

“Tokenholder(s)”

shall mean any person holding rightful legal ownership of the private key in relation to a Token.

 

“Website”

means www.ethena.fi.

 

1.2. In these Terms and Conditions, unless the context otherwise requires: references to these Terms and Conditions shall include any Schedules to it and references to Clauses, Sub-clauses and any Schedules are to Clauses of, Sub-clauses of, and any Schedules to these Terms and Conditions; the singular includes the plural and vice versa; “person” denotes any person, partnership, corporation or other association of whatever nature; and any references to any directive, statute, statutory instrument, laws or regulations shall be references to such directive, statute, statutory instrument, laws or regulations as from time to time amended, re-enacted or replaced and to any codification, consolidation, re-enactment or substitution thereof as from time to time in force and any reference to a regulator or public authority and rules made by it shall include its successor and rules made by the successor which replace those rules.

1.3. Headings are for convenience only and have no bearing on the interpretation of these Terms and Conditions.

1.4. Any phrase introduced by the term “include”, “includes”, “including”, “for example”, “in particular” or any similar expression will be construed as illustrative and will not limit the sense of the words preceding that term.

1.5. References to “dealing in” or “deal in” are references to any participation in crypto assets including buying, acquiring, accepting, holding, selling, staking, disposing of or otherwise making use of crypto assets.

## 2. KYC/AML Requirements and Onboarding (Greenlisting)

2.1. In order to purchase and/or redeem Tokens with the Issuer directly, a successful onboarding of the user and completion of the KYC/AML Requirements by the user providing all required data and including confirmation that the user is eligible is required.

2.2. All natural and legal persons as well as partnerships with a legal personality are eligible to purchase and/or redeem Tokens if they are not a Prohibited Person.

2.3. The following information is required for onboarding if the user is a natural person:

a) All names and surnames of the user;

b) the declared place of residence including the complete address;

c) the user’s date of birth;

d) the user’s place of birth;

e) the nationality of the user;

f) the copy of an identity card or passport which has been issued by the competent authority to the user;

g) an e-mail address of the user; and

h) information to validate the source of funds / wealth.

Additional information may be required in enhanced due diligence processes.

2.4. The following information will be required for onboarding, if the user is an entity or a partnership with a legal personality:

a) complete legal form of the user;

b) statuary, respectively the in a public registry registered, place of business of the user including the complete address;

c) (if existing) the user’s registry number from the commercial registry or a comparable public registry;

d) name of the statutory authorized representative or representatives of the user;

e) an e-mail address of the user; and

f) proper corporate records such as Certificate of Incorporation or Good Standing, director’s register and others.

Additional information may be required in enhanced due diligence processes.

2.5. As part of the onboarding process, the user is asked to name at least one blockchain address on any of the Blockchains to which the Tokens can be transferred after successful completion of the onboarding process. Users may be asked to provide confirmation of ownership or control of each wallet. Wallet screens may be conducted as part of the onboarding process and on an ongoing basis.

2.6. In order for the onboarding to be successful it is required that the information provided by the user is

a) complete; and

b) that there is no indication that the user provided incorrect data.

2.7. The Issuer is entitled, but not obligated, to have the data provided during the onboarding process audited by a qualified third party.

2.8. The Issuer notifies the user if the onboarding and the completion of the KYC/AML Requirements was successful. The respective user is then considered as Greenlisted.

2.9. The user is obligated to notify the Issuer immediately if any of the information provided has changed. The Issuer may require periodic updates to information provided, during which time the user’s status as Greenlisted will be probationary and may be revoked pending the outcome of such updates, or in the case where the user does not comply with requests for updated information.

## 3. Properties of the Tokens

3.1. The Token intends to maintain a relatively stable value approximating USDC and other dollar-pegged stablecoins by utilizing a delta-neutral hedging mechanism. The Token derives its relative peg stability from executing automated and programmatic delta-neutral hedges with respect to the underlying reserve assets consisting of Ethereum or Bitcoin provided by Greenlisted users. The hedging mechanism is described in more detail at https://ethena-labs.gitbook.io/ethena-labs.

3.2. Tokens are created on basis of the blockchain technology as units of value on any of the Blockchains being directly transferable between users following distribution by the Issuer.

3.3. The Tokens are not designed to intrinsically create returns for Tokenholders, increase in value, or otherwise accrue financial benefit to Tokenholders. Tokenholders will not earn any interest or other returns simply by virtue of holding Tokens. Tokens should therefore not be considered by users as investments.

3.4. The Tokens are fully fungible and may be traded on exchanges. The Tokens may also be traded on a bilateral (OTC) or Peer to Peer basis directly on the blockchain.

## 4. Ordering Procedure and Delivery of Tokens

4.1. The minimum amount to be acquired from the Issuer by each user is determined based on the gas price charged by the Blockchain at the time of mint. If the gas cost to mint an amount of USDe exceeds the value of the USDe to be minted, the mint transaction will not process. There is otherwise no minimum subscription amount.

4.2. Anyone wishing to receive Tokens requires a wallet that is compatible with any of the Blockchains. The Issuer cannot accept orders without specifying a blockchain address (public key) in the online subscription process. A smartphone or a computer with internet access is necessary to create a wallet.

4.3. The Tokens may be acquired from the Issuer by submitting a purchase application to the Issuer on the Website. The user must provide the intended purchase amount and its wallet address on any of the Blockchains to which its Tokens are to be transferred, which may be done by connecting the Blockchain wallet provided during the Greenlisting process to the Website.

4.4. The purchase amount is due immediately after the acceptance of the offer by the Issuer. The user shall pay the purchase amount to (i) the Issuer via transfer to the relevant Blockchain smart contract, or (ii) to the extent the Issuer enables minting with fiat currency, the bank account specified by the Issuer.

4.5. The Issuer’s receipt of payment can be confirmed to the user by e-mail or by other means, including displaying confirmations on the Website following successful submission of a mint transaction.

4.6. A Tokenholder may dispose of its Tokens. The respective transaction is traceable for everyone over the respective Blockchain. A Tokenholder is expressly prohibited from knowingly transferring any Tokens to a Prohibited Person following acquisition.

## 5. Listing and Trading of the Token

5.1. Currently, the Tokens are listed on certain “centralized” exchanges and are available via blockchain-based automated market maker applications. Tokenholders understand and acknowledge that:

a) there can be no assurances that the Tokens will be admitted to trading on an exchange or that such trading will continue indefinitely and nothing in these Terms and Conditions shall be construed as constituting a warranty or promise to that effect; and

b) unless Tokens are admitted to trading on a centralized exchange, the trading of Tokens will be possible only on a Peer-to-Peer basis.

5.2. The Issuer may at any time purchase Tokens from Tokenholders in the secondary market and may hold, resell or burn such Tokens. Any such purchase will be made on an arm’s length basis at the prevailing market price and in accordance with Applicable Law.

## 6. Exercise of Rights

6.1. The Issuer will recognize and acknowledge as Tokenholders only those persons who both (i) hold Tokens and (ii) have successfully completed the KYC/AML Requirements and are, at the time of determination under this paragraph, Greenlisted.

6.2. Various functionalities of the Tokens, including, but not limited to, the issuance and the transfer of Tokens and the redemption of the Tokens, are available only with the private key associated with the wallet controlling such Tokens. Each Tokenholder agrees that the Issuer shall not be held liable and waive any claim against the Issuer to the fullest extent permitted by Applicable Law, for any loss or damages resulting from the loss or theft of its private key, including, but not limited to, any claims for indirect or consequential and additional expenses.

## 7. Redemption

7.1. Every Tokenholder can request a redemption of all or part of their Tokens on demand at the value representing the Token’s share in the asset reserve. While the value of the underlying spot crypto asset may fluctuate, the Issuer employs hedging strategies to keep these fluctuations minimal as described in more detail at https://ethena-labs.gitbook.io/ethena-labs. Redemption requests will be satisfied by the Issuer in accordance with Applicable Laws. Where the withdrawal payment is received by a Tokenholder through the involvement of a payment service provider, the Issuer shall not be responsible for the withdrawal payment once the withdrawn funds are received by the payment service provider of the Issuer.

7.2. From January 01, 2025 onwards USDe will be issued and redeemed by two separate legal entities (Dual Issuers): 

* Ethena GmbH, Germany, will issue and redeem USDe for users in the European Economic Area (EEA).
* Ethena BVI Limited, British Virgin Islands, will issue and redeem USDe for users in all counties outside the EEA.

General Rule 

The holders of USDe that are residents of the EEA, or have their registered office in the EEA can redeem their USDe with Ethena GmbH only. They have a right of redemption according to the conditions and processes for redemption of USDe that are described in Ethena GmbH’s Terms and Conditions, Section 7 “Redemption.” The holders of USDe who have their residence or registered office outside of the EEA can redeem their USDe with Ethena BVI Limited only. They have a right of redemption according to the specific USDe terms and conditions of Ethena BVI Limited, a British Virgin Islands limited liability company. 

If you have your residence or registered office outside of the European Economic Area (EEA), Ethena BVI Limited will become your new contractual partner if you agree according to Section 20.4. of these Terms and Conditions. In this case, your contract with Ethena GmbH will be transferred to Ethena BVI Limited. Your consent also includes the transfer of customer data from Ethena GmbH to Ethena BVI Limited for this purpose.

Verification of country of residence or registered office 

When a USDe holder requests the redemption of their USDe, Ethena GmbH will verify the USDe holder’s country of residence or registered office according to the documents the USDe holder had provided during the onboarding process (Greenlisting). These are detailed in Section 2 „KYC/AML Requirements and Onboarding (Greenlisting)“ of Ethena GmbH’s Terms and Conditions. 

A USDe holder who is resident in the EEA may not yet have been onboarded and greenlisted, e.g. those who acquired their USDe on secondary markets. If such USDe holders request their USDe to be redeemed by Ethena GmbH, they must first complete the „KYC/AML Requirements and Onboarding (Greenlisting)“ process described in Section 2 of Ethena GmbH’s Terms and Conditions. 

7.3. Every withdrawal request is subject to withdrawal limits. These limits are adjusted dynamically depending on the type of identification documentation required, as well as market conditions. If a withdrawal request exceeds the current limit, the Issuer may decline the request and instead require the Tokenholder to submit documents verifying its identity and address prior to allowing a withdrawal of funds or to otherwise cooperate with the Issuer to verify its identity or to submit a new request in line with market conditions, if applicable.

7.4. Every Tokenholder must ensure that the payment details it enters when redeeming Tokens are correct and complete. The Issuer is not liable for withdrawn assets being sent to the wrong account where this is due to the Tokenholder providing incorrect payment details.

7.5. No redemption transaction is processed until a Tokenholder requests, and is provided with, a price quote by submitting such request on app.ethena.fi. The price quote is determined by assuming, as a baseline, that 1 USDe = 1 USDC; however, in the case where an adverse event has occurred that reduces the value of the asset reserve, the price quote will include a reduction to reflect a pro-rata reduction in the redemption pricing accordingly, and the pricing quote displayed to the user includes a reimbursement charge of 10 basis points. This charge is not retained by the Issuer for its own account and is intended solely to cover certain costs associated with the architecture, namely execution costs for hedges and blockchain gas fees.

## 8. Limited Recourse

Notwithstanding anything to the contrary herein, no recourse (whether by institution or enforcement of any legal proceeding or assessment or otherwise) in respect of any breaches of any duty, obligation or undertaking of the Issuer arising under or in connection with the Tokens (as from time to time supplemented or modified in accordance with the provisions herein contained) by virtue of any law, statute or otherwise shall be held against any shareholder, officer, manager or corporate services provider of the Issuer in their capacity as such, save in the case of their gross negligence, willful default or actual fraud, and any and all personal liability of every such shareholder, officer, manager of corporate services provider in their capacity as such for any breaches by the Issuer of any such duty, obligation or undertaking shall be waived and excluded to the extent permitted by law.This provision shall survive the redemption and burning of the Tokens.

## 9. Modification of the Smart Contract

9.1. The smart contract underlying the Tokens may have a mechanism that allows the Issuer (or an affiliate of the Issuer) to modify the corresponding source code. However, this mechanism may only be used in order to

a) address security issues of the underlying smart contract;

b) correct unintended deviations from the provisions of these Terms and Conditions;

c) change the structure of the source code, class interfaces, control flow, as far as this does not contradict these Terms and Conditions; or

d) change elements of the smart contract that have become ineffective or impractical due to external effects.

9.2. If changes to the smart contract are required pursuant to Condition 9.1, the Issuer shall be entitled to amend these Terms and Conditions accordingly. The Tokenholders shall be notified of any such amendments with a notice according to Condition 13 (Notice).

## 10. Substitution of the Issuer

10.1. The Issuer may, without the consent of the Tokenholders, at any time substitute itself in respect of all rights and obligations arising under or in connection with the Tokens with any legal entity of which all shares carrying voting rights are directly or indirectly held by the Issuer (the “New Issuer”), provided that:

a) the New Issuer is able to fulfil all payment obligations arising from or in connection with the Tokens; and

b) the Issuer has issued an irrevocable and unconditional guarantee in respect of the obligations of the New Issuer under the Tokens.

10.2. In the event of a substitution of the Issuer, notice of such substitution shall be made in accordance with Condition 13 (Notice) and any reference to the Issuer shall be deemed to refer to the New Issuer.

## 11. No Set-off

No Tokenholder may set-off any claims arising under the Tokens against any claims that the Issuer may have against it. The Issuer may not set-off any claims it may have against the Tokenholder against any of its obligations under the Tokens.

## 12. Modification Clause

12.1. If these Terms and Conditions contain manifest typographical errors or misspellings, the Issuer shall be entitled to correct such errors or misspellings without obtaining the Tokenholders’ consent, provided that such correction, taking into account the Issuer’s interests, can reasonably be assumed to be acceptable to the Tokenholders and, in particular, does not materially adversely affect the Tokenholders’ legal and financial position. Any such corrections shall be announced to the Tokenholders in accordance with Condition 13 (Notice).

12.2. If these Terms and Conditions contain manifest calculation errors, the Issuer shall be entitled to correct such errors without obtaining the Tokenholders’ consent, provided that such correction, taking into account the Issuer’s interests, can reasonably be assumed to be acceptable to the Tokenholders and, in particular, does not materially adversely affect the Tokenholders’ legal and financial position. Any such corrections shall be announced to the Tokenholders in accordance with Condition 13 (Notice).

12.3. If these Terms and Conditions contain any similar manifest errors, the Issuer shall be entitled to correct such errors without obtaining the Tokenholders’ consent, provided that such correction, taking into account the Issuer’s interests, can reasonably be assumed to be acceptable to the Tokenholders and, in particular, does not materially adversely affect the Tokenholders’ legal and financial position. Any such corrections shall be announced to the Tokenholders in accordance with Condition 13 (Notice).

12.4. Any other inconsistencies or omissions in these Terms and Conditions may be corrected or supplemented by the Issuer in its reasonable discretion (Section 315 BGB). However, only such corrections or supplements shall be permitted as – taking into account the Issuer’s interests – can reasonably be assumed to be acceptable to the Tokenholders and, in particular, do not materially adversely affect the Tokenholders’ legal and financial position. Any such corrections or supplements shall be announced to the Tokenholders in accordance with Condition 13 (Notice).

12.5. Manifest typographical errors or misspellings and similar manifest errors in these Terms and Conditions shall entitle the Issuer to a right of avoidance (Anfechtung) vis-à- vis the Tokenholders. Such right of avoidance may only be exercised consistently vis-à-vis all Tokenholders and without undue delay after having become aware of the relevant reason entitling to the right of avoidance. The right of avoidance shall be exercised by announcement in accordance with Condition 13 (Notice).

12.6. Manifest calculation errors and similar manifest errors in these Terms and Conditions shall entitle the Issuer to a right of avoidance (Anfechtung) vis-à-vis the Tokenholders. Such right of avoidance may only be exercised consistently vis-à-vis all Tokenholders and without undue delay after having become aware of the relevant reason entitling to the right of avoidance. The right of avoidance shall be exercised by announcement in accordance with Condition 13 (Notice).

## 13. Notice

All notices regarding the Tokens shall be published on the Website.

## 14. Taxes

14.1. All payments made by or on behalf of the Issuer in respect of the Tokens will be made free from any restriction or condition and be made without deduction or withholding for or on account of any present or future taxes, duties, assessments or governmental charges of whatever nature imposed or levied by or on behalf of the Federal Republic of Germany, unless deduction or withholding of such taxes, duties, assessments or governmental charges is required to be made by Applicable Law.

14.2. The tax treatment for each user depends on the particular situation. All users are advised to consult with their professional tax advisers as to the respective German tax consequences of the purchase, ownership, disposition, lapse, exercise or redemption of Tokens in light of their particular circumstances.

## 15. Intellectual Property Rights

15.1. The Issuer and its affiliated companies own all intellectual property and other rights in each of the products and its respective contents, including, but not limited to, software, text, images, trademarks, service marks, copyrights, patents, designs, and its look and feel. This intellectual property is available under the terms of our copyright licenses and our trademark guidelines. Subject to these Terms and Conditions, the Issuer and its affiliated companies grant the users a limited, revocable, non-exclusive, non-sublicensable, non-transferable license to access and use their products solely in accordance with these Terms and Conditions. You agree that you will not use, modify, distribute, tamper with, reverse engineer, disassemble or decompile any of our products for any purpose other than as expressly permitted pursuant to these Terms and Conditions. Except as set forth in these Terms and Conditions, the Issuer and its affiliated companies grant the users no rights to any of their products, including any intellectual property rights.

15.2. By using any of the products of the Issuer or its affiliated companies, users grant them a worldwide, non-exclusive, sublicensable, royalty-free license to use, copy, modify, and display any content, including but not limited to text, materials, images, files, communications, comments, feedback, suggestions, ideas, concepts, questions, data, or otherwise, that users post on or through any of the products of the Issuer or its affiliated companies for current and future business purposes of the Issuer or its affiliated companies, including to provide, promote, and improve the services.

## 16. Limitation of Liability

16.1. Unless explicitly otherwise provided in these Terms and Conditions, (i) any right of you to rescind from these Terms and Conditions; (ii) any claim for defects of a purchase object under Sections 437 through 441 BGB; (iii) any claim for breach of pre-contractual obligations (culpa in contrahendo, Sections 241 (2), 311 (2) (3) BGB); and (iv) any claim for frustration of contract pursuant to Section 313 BGB, shall be excluded, save for any remedies of you based on willful deceit, intentional breach of contract or gross negligence, provided, however, that our liability for willful deceit, intentional breach of contract or gross negligence of any person assisting us in the performance of our obligations in the meaning of Section 278 BGB shall be excluded.

16.2. Unless explicitly stated otherwise in these Terms and Conditions, the Issuer shall not be held liable for any damages, losses, claims, costs, expenses or other liabilities, whether direct, indirect, consequential or otherwise, arising from the conduct of any third party not directly under the control and supervision of the Issuer including, but not limited to, independent contractors, partners, affiliates, suppliers, banks, brokerage firms, customers, or any other third parties interacting with, or acting on behalf of, the Issuer. Notwithstanding the foregoing, nothing in this Condition shall limit or exclude the Issuer’s liability where the third party was acting under the direct instruction, authority, or control of the Issuer, or where the conduct of the third party was otherwise foreseeable and preventable.

16.3. In the case of simple negligence, the Issuer shall only be liable for damages arising from injury to life, body, or health, as well as for damages arising from the breach of a material contractual obligation (cardinal duty). A material contractual obligation is an obligation whose fulfillment is essential for the proper execution of the contract and on whose compliance the contractual partner regularly relies. In such cases, the liability of the Issuer shall be limited to the typical, foreseeable damage.

## 17. Non-Custodial and No Fiduciary Duties

17.1. We do not ever have custody, possession, or control of your digital assets at any time. You are solely responsible for the custody of the cryptographic private keys to the digital asset wallets you hold, and you should never share your wallet credentials or seed phrase with anyone. We accept no responsibility for, or liability to you, in connection with your use of a wallet. Likewise, you are solely responsible for any associated wallet and we are not liable for any acts or omissions by you in connection with or as a result of your wallet being compromised.

17.2. These Terms and Conditions is not intended to, and does not, create or impose any fiduciary duties on us. To the fullest extent permitted by law, you acknowledge and agree that we owe no fiduciary duties or liabilities to you or any other party, and that to the extent any such duties or liabilities may exist at law or in equity, those duties and liabilities are hereby irrevocably disclaimed, waived, and eliminated. You further agree that the only duties and obligations that we owe you are those set out expressly in these Terms and Conditions.

## 18. Governing Law and Jurisdiction

18.1. These Terms and Conditions and the Tokens are exclusively subject to the laws of the Federal Republic of Germany with the exclusion of the conflict-of-law rules of the international private law and the UN sales convention (CISG).

18.2. The place of performance and sole legal venue for all disputes arising from the legal relationships regulated under these Terms and Conditions is the respective business seat of the Issuer unless mandatory statutory provisions contradict and the parties are merchants, legal persons under public law or a special fund under public law or at least one of the parties has no place of general jurisdiction within the Federal Republic of Germany. The Issuer’s business seat at the time of the first launch of the Tokens is in Hamburg.

## 19. Severability

If at any time one or more of the provisions of these Terms and Conditions is or becomes unlawful, invalid, illegal or unenforceable in any respect under any Applicable Law, the validity, legality and enforceability of the remaining provisions shall not be in any way affected or impaired thereby.

## 20. Miscellaneous

20.1. We do not provide, nor do we accept responsibility for, any legal, tax or accounting advice. If you are unsure regarding any of the legal, tax or accounting aspects of these Terms and Conditions or dealing in Tokens you should seek independent professional advice.

20.2. No waiver or variation of any part of these Terms and Conditions by us shall be effective unless in writing and signed by us. No waiver of any provision in these Terms and Conditions will be deemed a waiver of a subsequent breach of such provision or a waiver of a similar provision. In addition, a waiver of any breach or a failure to enforce any term or condition of these Terms and Conditions will not in any way affect, limit, or waive our rights hereunder at any time to enforce strict compliance thereafter with every term and condition of these Terms and Conditions.

20.3. No other document or communication may modify or add any additional obligations or covenants on us beyond those set forth in these Terms and Conditions, unless we clearly, specifically and explicitly state otherwise in that document.

20.4. USDe Terms and Conditions may change from time to time. If you have been onboarded and greenlisted with Ethena GmbH, you will be notified of any changes to these USDe Terms and Conditions and their effective date by an electronic message sent to the electronic address you have provided as part of your onboarding process for communication with Ethena GmbH. 

You have the right to terminate the contract without notice and free of charge within the aforementioned two months period. 

If you reject any of these changes to the USDe Terms and Conditions, we may either continue the contract under the previous terms or terminate the contract with a notice period of two months.

Last updated 4 months ago

Was this helpful?

---


# USDe Terms and Conditions - Non EEA

Source: https://docs.ethena.fi/resources/usde-terms-and-conditions-non-eea

Last Updated: January 2025

Users who have completed Know-Your-Customer and Anti-Money Laundering checks, as well as other onboarding procedures, and are whitelisted with Ethena BVI Limited (“Ethena BVI”) are referred to herein as a “Mint User.” To the extent you have not completed the aforementioned checks or been whitelisted but hold USDe, these Terms still apply to your holding and use of USDe (hereinafter referred as “Holding User”). For the avoidance of doubt, Holding Users are not customers of Ethena BVI.

By obtaining and using USDe, you understand and expressly agree to these Terms, regardless of whether or not you are a customer of Ethena BVI, and you acknowledge that you have reviewed and understand each of the disclosures made in this section. Any provisions of these Terms that only apply to Mint Users or Holding Users will be specifically noted herein. Unless so noted, each Section of these Terms apply to both Mint Users and Holding Users, and any use of “you” or “your” refers to both Mint Users and Holding Users. The terms herein applicable to Mint Users are supplemental to the terms in the USDe Mint User Agreement.

By holding or using USDe, or using any of the USDe Services, you agree that you have read, understood and accept all of the terms and conditions contained in these Terms, as well as our Privacy Policy and Cookie Policy, and you acknowledge and agree that you will be bound by these terms and policies.

Section 22 of these Terms governs how these Terms may be changed over time; the date of the last update is set forth at the top of these Terms.

**1. About USDe**

USDe is a digital token issued by Ethena BVI. USDe issued by Ethena BVI is a form of stored value or prepaid access and does not represent a claim, participation interest, economic right, voting right, or other similar right associated with Ethena BVI or any of its affiliates.

USDe is backed by an amount of spot crypto assets, such as BTC, ETH, SOL, certain stablecoins (such as USDC, USDT, and USDtb), and offsetting hedging positions on derivatives contracts the (“USDe Reserves”). Ownership of the USDe Reserves lies with the Ethena Foundation, an unaffiliated third party, which provides Ethena BVI with a license to hold and administer the USDe Reserves. The Ethena Foundation does not have any members, ultimate beneficial owners, or beneficiaries, and exists with the principal objects of supporting the Ethena Protocol and its architecture. No shareholders, employees, contractors, ultimate beneficial owners, or other party affiliated with Ethena BVI or its affiliates holds a position of ownership or control with respect to the Ethena Foundation. USDe is not designed to intrinsically create returns for holders, increase in value, or otherwise accrue financial benefit to the USDe holder.

**2. Scope of USDe and Key Terms**

The following only applies to Mint Users: As you have agreed to, and are subject to, the USDe Mint User Agreement, Ethena BVI makes available the following USDe-related Services (as defined in the USDe Mint User Agreement: (i) issue USDe for accepted tokens from Ethena BVI, and (ii) redeem USDe for supported assets from Ethena BVI (collectively, the “USDe Services”). Your use of the USDe Services is subject to these Terms. Any of the USDe Services can be discontinued at any time in accordance with Section 14 of these USDe Terms.

You understand and agree that you may only tokenize accepted assets for USDe and redeem USDe directly with Ethena BVI to the extent that you are a Mint User.

The following only applies to Holding Users: You may not redeem USDe with Ethena BVI unless and until you are a Mint User who has cleared KYC/AML and other checks and have onboarded as a whitelisted customer with Ethena BVI. Eligibility for and requirements related to such process are set forth in the USDe Mint User Agreement.

The following applies to both Mint Users and Holding Users: Your use of USDe and USDe Services (as applicable), is subject to these Terms and Ethena BVI’s obligations hereunder are conditional on you complying with its provisions. You understand that any violation of these Terms may result in potential consequences, including the possible loss or forfeiture of assets tokenized for USDe.

You understand and agree that sending USDe to another address automatically transfers and assigns to the owner of that address , and any subsequent owner all rights and obligations of a Holding User to redeem USDe for approved assets so long as the Holder is or becomes a Mint User. For the avoidance of doubt, if a Holder is not a Mint User, not eligible to become a Mint User, or fails to do so, such Holding User is not entitled to redeem USDe with Ethena BVI.

Ethena BVI (or an affiliate designated by Ethena BVI) commits to redeem 1 USDe for the notional value relating to its pro rata portion of the USDe Reserves in supported digital assets, subject to these Terms, applicable law, and any fees where applicable. While Ethena BVI may hold the USDe Reserves in interest-bearing accounts or other yield-generating instruments, you acknowledge that you are not entitled to any interest or other returns earned on such funds. USDe does not itself generate any interest or return for holders of USDe and only represents your right to redeem USDe as a Mint User, if you are one. If you are a Holding User, you do not have a right to redeem USDe with Ethena BVI.

**3. Applicable Laws and Regulations; AML and CTF**

Your holding and use of USDe, and any use of the USDe Services, is subject to the laws, regulations, and rules of any applicable governmental or regulatory authority, including, without limitation, all applicable tax, anti-money laundering (“AML”) and counter-terrorist financing (“CTF”) provisions and sanctions. You agree to act in compliance with and be legally bound by these Terms and all applicable laws and regulations. These Terms are conditional on your continued compliance at all times with these Terms and all applicable laws and regulations.

Ethena BVI is committed to complying with all applicable AML and CTF laws and regulations. These standards are designed to prevent the use of the USDe Services for money laundering, terrorist financing, fraudulent transactions, and any other illegal activities. Ethena BVI takes compliance very seriously and actively engages in measures to:

• Prohibit fraudulent transactions;

• Report suspicious activities;

• Prevent money laundering, terrorist financing, and any related acts that facilitate financial crimes.Applicable laws require us to prevent Restricted Persons from holding USDe or using USDe Services. A Restricted Person means any person that is the subject or target of any sanctions, including a person that is:

* named in any Sanctions-related list maintained by the U.S. Department of State; the U.S. Department of Commerce, including the Bureau of Industry and Security’s Entity List and Denied Persons List; or the U.S. Department of the Treasury, including the OFAC Specially Designated Nationals and Blocked Persons List, the Sectoral Sanctions Identifications List, and the Foreign Sanctions Evaders List; or any similar list maintained by any other relevant governmental authority;
* located, organized or resident in a country, territory or geographical region which is itself the subject or target of any territory-wide Sanctions (a “Restricted Territory”) (currently, Cuba, Iran, Syria, North Korea, and the Ukraine regions of Crimea, Donetsk, and Luhansk); or
* owned or controlled by any such person or persons listed above.

**4. Eligibility; Limitations**

The following applies to both Mint Users and Holding Users: USDe Services and support for USDe are currently only available to individuals and institutions (as applicable) located in supported jurisdictions.

By holding or using USDe, or accessing or using the USDe Services, you further represent and warrant that:

* you are at least 18 years old, are not a Restricted Person, and are not holding USDe on behalf of a Restricted Person.
* you will not be using USDe or the USDe Services (as applicable) for any illegal activity, including, but not limited to, illegal gambling, money laundering, fraud, blackmail, extortion, ransoming data, terrorism financing, other violent activities or any prohibited market practices, including, but not limited to, those listed under Sections 16 and 17.

Additionally, users in the United States are not eligible to become a Mint User. This restriction may be revisited from time to time taking into account relevant changes in law.

You also understand that there are additional representations and warranties made by you elsewhere in (or by reference in) these Terms and that any misrepresentation by you is a violation of these Terms.

If Ethena BVI suspects or determines that you or any of your authorized users or customers, as applicable, have violated these Terms, including, but not limited to, attempting to transact or transacting with Blocked Addresses (as defined in Section 11) or attempting to engage or engaging in Restricted Activities (as defined in Section 16) or Prohibited Transactions (as defined in Section 17), then Ethena BVI may be forced to terminate your status as a Mint User and you may forfeit any assets otherwise eligible for redemption.

Notwithstanding the foregoing, Ethena BVI may determine not to make USDe or the USDe Services, in whole or in part, available in every market, either in its sole discretion or due to legal or regulatory requirements, depending on your location. We may also, without liability to you or any third party, refuse to let you register as a Mint User.

The following only applies to Mint Users: Use of certain USDe Services may have further eligibility requirements that will need to be verified prior to you using such USDe Services, or from time to time in order to continue your use of the USDe Services, and may be subject to additional terms and conditions.

**5. Support**

Please contact Support to report any violations of these Terms or to ask any questions regarding these Terms or the USDe Services, as applicable.

**6. Copies, Wrappers, and Forks Not Supported**

The following applies to both Mint Users and Holding Users: As a result of the decentralized and open source nature of USDe it is possible that a party unaffiliated with Ethena BVI could create an alternative, equivalent version of USDe either on one of the USDe supported blockchains or on an unsupported blockchain (a “copy”) that operate independently from USDe. Similarly, it is possible that a party unaffiliated with Ethena BVI may create an asset and purport that such asset is collateralized by or otherwise incorporates USDe into its design (a “wrapper”). Ethena BVI supports only USDe and is under no obligation to support any copies of USDe or wrappers and assumes no responsibility for any value that might be lost as a result of this lack of support of copies of USDe. No such copy or wrapper should be considered approved, sold, distributed, or promoted by Ethena BVI unless explicitly stated.

As a result of the decentralized and open source nature of the blockchains on which USDe is supported, it is possible that a party unaffiliated with Ethena BVI could create an alternative version of the blockchain (a “fork”). Note that in the event of a fork of one of the USDe supported blockchains, Ethena BVI may be forced to suspend all activities relating to USDe (including tokenizing assets for USDe, redeeming USDe for supported assets, or sending and receiving USDe) for an extended period of time until Ethena BVI has determined in its sole discretion that such functionality can be restored (“Downtime”). This Downtime will likely occur immediately upon a “fork”, potentially with little to no warning, and during this period of Downtime you will not be able to conduct various activities involving USDe. In the event of a fork of one of the USDe supported blockchains, Ethena BVI shall, in its sole discretion, determine which fork it will support, if any.

**7. USDe Supported Blockchains and Smart Contract Modifications**

USDe operates on USDe supported blockchains. Ethena BVI does not have any ability or obligation to prevent or mitigate attacks or resolve any other issues that might arise with any USDe supported blockchain. Any such attacks or delays on any USDe supported blockchain might materially delay or prevent you from sending or receiving USDe, and Ethena BVI shall bear no responsibility for any losses that result from such issues.

Note that in certain circumstances, including, but not limited to, a copy or fork of a USDe supported blockchain or the identification of a security issue with a USDe supported blockchain, Ethena BVI may be forced to suspend all activities relating to USDe (including tokenizing assets for USDe, redeeming USDe for assets, or sending and receiving USDe) for an extended period of time until such Downtime is over and USDe Services can be restored. This Downtime will likely occur immediately upon a copy or fork of any USDe supported blockchain, potentially with little to no warning, and during this period of Downtime you will not be able to conduct various activities involving USDe.

Ethena BVI reserves the right to migrate USDe to another blockchain or protocol in the future in its reasonable discretion. Upon Ethena BVI’s request, you agree to take any and all actions reasonably necessary to effectuate the migration of your USDe to another blockchain or protocol identified by Ethena BVI. Ethena BVI will not be responsible or liable for any damages, losses, costs, fines, penalties or expenses of whatever nature, whether or not reasonably foreseeable by the parties, which you may suffer, sustain or incur, arising out of or relating to your failure to effectuate such migration of your USDe to another blockchain or protocol identified by Ethena BVI.

**8. Privacy**

We are committed to protecting your personal information and helping you understand exactly how your personal information is being used. You should carefully read the Ethena BVI Privacy Policy, as it provides details on how your personal information is collected, stored, protected, and used.

**9. Communications**

By entering into these Terms, you agree to receive electronic communications and notifications.

These Terms are provided to you and communicated in English. We will also communicate with you in English for all matters related to USDe and your use of USDe Services. Where we have provided you with a translation of the English language version of these Terms, you agree that such translation is provided for your convenience only and that the English language version of these Terms govern your holding and use of USDe, and the USDe Services, as applicable.

**10. Limited License; IP Rights**

The following only applies to Mint Users: We grant you a limited, non-exclusive, non-sublicensable, and non-transferable license, subject to the terms and conditions of these Terms, to access and use the USDe Services solely for approved purposes as determined by Ethena BVI. Any other use of the USDe Services is expressly prohibited. Ethena BVI and its licensors reserve all rights in the USDe Services and you agree that these Terms does not grant you any rights in or licenses to the USDe Services except for the limited license set forth above. Except as expressly authorized by Ethena BVI, you agree not to modify, reverse engineer, copy, frame, scrape, rent, lease, loan, sell, distribute, or create derivative works based on the USDe Services, in whole or in part. If you violate any portion of these Terms, your permission to access and use the USDe Services may be terminated pursuant to these Terms.

"ethena.fi", "Ethena BVI", and all logos related to the USDe Services are either copyrights, trademarks, or registered marks of Ethena BVI or its licensors. Whether or not you are a Mint User, you may not copy, imitate, or use them without Ethena BVI's prior written consent. All right, title, and interest in and to the Ethena BVI website, any content thereon, the USDe Services, and all technology and any content created or derived from any of the foregoing is the exclusive property of Ethena BVI and its licensors.

**11. Risk Factors & Disclosures**

The following list of risks associated with USDe and the USDe Services is not exhaustive.

No guarantee of price stability on Third Party Platforms

Ethena BVI does not guarantee that the value of one (1) USDe will always or ever equal 1 USD ($1) on any platform. Due to a variety of factors, the value of USDe on third-party platforms such as cryptocurrency exchange platforms could fluctuate above or below 1 USD ($1), and the risk factors highlighted at docs.ethena.fi (as well as presently unknown risk factors) may result in the USDe Reserves falling to less than 1 USD ($1) of notional value per USDe in circulation. Ethena BVI cannot control how third parties quote or value USDe, and Ethena BVI is not responsible for any losses or other issues that may result from fluctuations in the value of USDe.

Third-parties

Ethena BVI does not control or endorse any products, services, or platforms offered by third parties using the USDe Services or supporting USDe. Third parties may elect to support USDe on their platforms without any authorization or approval by Ethena BVI. The availability of USDe on any third-party platform does not imply that such services are valid, legal, stable, or otherwise appropriate.

Ethena BVI is not liable for any losses, issues, or consequences that may arise from third-party transactions or the use of USDe on third-party platforms, including, but not limited to, (i) Failure to comply with applicable laws and regulations, including illegal transactions;(ii) The quality, delivery, or satisfaction of products and services facilitated by USDe Services; (iii) Technical errors, loss of access, or inability to recover USDe resulting from the use of third-party platforms.

You accept all consequences of sending USDe to third-party platforms or addresses, including the risk of loss or failure to recover your USDe. For the avoidance of doubt, Ethena BVI has no obligation to track, verify, or determine the provenance of USDe balances or transactions involving third-party platforms.

You accept all consequences of sending USDe

USDe transactions are not reversible. Once you send USDe to an address, you accept the risk that you may lose access to, and any claim on, that USDe indefinitely or permanently. For example, (i) an address may have been entered incorrectly and the true owner of the address may never be discovered, (ii) you may not have (or subsequently lose) the private key associated with such address, (iii) an address may belong to an entity that will not return the USDe, or (iv) an address belongs to an entity that may return the USDe but first requires action on your part, such as verification of your identity. For the avoidance of doubt, nothing in these Terms is intended to obligate Ethena BVI to track, verify or determine the provenance of USDe balances for Users, including any form of security interests claimed thereon.

Blocked Addresses & Forfeited Funds

Ethena BVI reserves the right to “block” certain USDe addresses of Mint Users that it determines, in its sole discretion, may be associated with illegal activity or activity that otherwise violates these Terms (“Blocked Addresses”). In certain circumstances, Ethena BVI may deem it necessary to report such suspected illegal activity to applicable law enforcement agencies and you may forfeit any rights associated with your USDe, including the ability to redeem USDe for any permitted assets. Ethena BVI may also be required to surrender associated assets held in the USDe Reserve in the event it receives a legal order from a valid government authority requiring it to do so.

Software protocols and operational challenges

You are aware of and accept the risk of operational challenges. Ethena BVI may experience sophisticated cyber-attacks, unexpected surges in activity or other operational or technical difficulties that may cause interruptions to the USDe Services. You understand that the USDe Services may experience operational issues that lead to delays, including delays in redeeming USDe. You agree to accept the risk of transaction failure resulting from unanticipated or heightened technical difficulties, including those resulting from sophisticated attacks. You agree not to hold Ethena BVI accountable for any related losses.

Compliance

You are responsible for complying with applicable law. You agree that Ethena BVI is not responsible for determining whether or which laws may apply to your transactions, including tax laws. You are solely responsible for reporting and paying any taxes arising from your use of USDe or the USDe Services, including any accurate reporting of the tax or legal status of USDe in your jurisdiction.

Legal treatment of USDe transfers

The regulatory status of USDe and blockchain technology is unclear or unsettled in many jurisdictions. It is difficult to predict how or whether regulatory agencies may apply existing regulation with respect to USDe, blockchain technology and its applications. Accordingly, it is not possible to determine whether a USDe transfer would be recognized under applicable law by a court or regulator.

Legislative and regulatory changes

Legislative and regulatory changes or actions at the international level may adversely affect the tokenization of assets into USDe, and the use, transfer, redemption and/or value of USDe.

No deposit insurance

USDe held in your wallet is not subject to deposit insurance protection, including, but not limited to, (i) where your country of residence is the United States, the Federal Deposit Insurance Corporation (FDIC) insurance or Securities Investor Protection Corporation protections (SIPC); or (ii) where your country of residence is outside of the United States, the United Kingdom Financial Services Compensation Scheme (FSCS) or equivalent scheme in your country of residence.

Claim on funds

Only Mint Users can redeem USDe directly with Ethena BVI. For Mint Users, your ability to redeem with us for each USDe is conditional on (i) your possession of a corresponding amount of USDe associated with a Mint User, (ii) no violation of these Terms or your USDe Mint User Agreement, and (iii) no action, pending or otherwise, by a regulator, law enforcement or a court of competent jurisdiction that would restrict redemption.

Sending USDe to another address automatically transfers and assigns to that Holding User, and any subsequent Holding User, the right to redeem USDe with us so long as the Holding User is eligible to, and does, register as a Mint User (and thereby becomes a Mint User).

Encumbrances

Depending on the actions of the owners of USDe addresses before your receipt of USDe from another USDe address, it is possible that the transfer of USDe between USDe addresses could result in the USDe in your whitelisted wallet becoming subject to a lien or other form of security interest before redemption.

On-chain transactions irreversible

When USDe is sent to a third-party USDe address, such transaction is completed on USDe supported blockchains. This means that such a transaction is irreversible and Ethena BVI does not have the ability to reverse or recall any transaction once initiated. You bear all responsibility for any losses that might be incurred as a result of sending USDe to an incorrect or unintended USDe address.

Affiliate Activities

You understand and agree that individuals or entities affiliated with Ethena BVI may hold, purchase, sell, or otherwise engage in transactions using or involving USDe. You further understand and agree that such persons may engage in this activity for any reason, including but not limited to engaging in commercial transactions, promoting transaction activity that utilizes USDe, or otherwise supporting the use or adoption of USDe. This activity may involve selling USDe to other entities for provision to their end users. You understand and agree that no individual or entity, whether affiliated with Ethena BVI or otherwise, is under any obligation to engage in these activities, and they may be discontinued at any time.

**12. Fees; Authorization**

The following only applies to Mint Users: Except as disclosed to you prior to completing a transaction as a Mint User, Ethena BVI will not charge you any fees for tokenizing assets for USDe, or receiving USDe. Any cost of executing a mint or redemption transaction is a cost reimbursement to cover friction such as blockchain gas fees or execution fees paid by Ethena BVI.

**13. Currency Conversion**

The following only applies to Mint Users: All tokenizations of assets will be credited in USDe to your whitelisted wallet(s) based on a rate of one (1) USDe per 1 USD ($1) of notional value (measured in stablecoin value, i.e., 1 USDC, 1 USDT, or 1 USDtb, as the case may be, depending on the asset exchanged to mint USDe), less applicable fees and transaction costs associated with the transaction, including, for the avoidance of doubt, fees paid associated with the applicable blockchain consensus mechanism. Such value shall be calculated by Ethena BVI based on the asset in its sole discretion, with any transaction fees associated with the blockchain consensus mechanism determined by requirements of the underlying blockchain at the time the transaction is submitted by the Mint User.

**14. Right to Change/Remove Features or Suspend/Delay Transactions**

The following only applies to Mint Users: We reserve the right to (i) change, suspend, or discontinue any aspect of the USDe Services at any time, including hours of operation or availability of any feature, without notice and without liability and (ii) decline to process any issuance or redemption without prior notice and may limit or suspend your use of one or more USDe Services at any time, in our sole discretion. Our rights under this paragraph are subject to our obligations under applicable law and licenses, including but not limited to our reasonable suspicion of inappropriate or illegal conduct. Suspension of your use of any of the USDe Services will not affect your rights and obligations pursuant to these Terms. We may, in our sole discretion, delay issuances or redemptions if we reasonably believe the transaction is suspicious, may involve fraud or misconduct, violates applicable laws, or violates the terms of these Terms.

**15. Transactions Irreversible**

The following only applies to Mint Users: Once a transaction has been initiated, it cannot be reversed, as further described in Section 11 above and pursuant to the underlying blockchain consensus mechanism. Except as set forth in these Terms, all transactions processed through the USDe Services are nonrefundable.

**16. Restricted Activities**

In connection with your holding or use of USDe, or the USDe Services (as applicable), you hereby agree that you will not:

* violate (or assist any other party in violating) any applicable law, statute, ordinance, or regulation;
* intentionally try to defraud (or assist in the defrauding of) Ethena BVI or other Mint Users or Holding Users;
* provide false, inaccurate, or misleading information;
* take any action that interferes with, intercepts, or expropriates any system, data, or information;
* partake in any transaction involving the proceeds of illegal activity;
* transmit or upload any virus, worm, or other malicious software or program;
* attempt to gain unauthorized access to the Ethena BVI website, or any related networks or systems;
* use the USDe Services on behalf of any third party or otherwise act as an intermediary between Ethena BVI and any third parties;
* collect any information from other Mint Users or Holding Users, including, without limitation, email addresses;
* defame, harass, or violate the privacy or intellectual property rights of Ethena BVI or any Holding Users or Mint Users; or
* upload, display or transmit any messages, photos, videos or other media that contain illegal goods, violent, obscene or copyrighted images or materials (such activities, “Restricted Activities”).

**17. Prohibited Transactions**

Using USDe or the USDe Services for transactions related to the following is prohibited, and Ethena BVI reserves the right to monitor and, if appropriate, block or otherwise prevent transactions that relate to:

* any Restricted Persons;
* weapons of any kind, including but not limited to firearms, ammunition, knives, explosives, or related accessories;
* controlled substances, including but not limited to narcotics, prescription drugs, steroids, or related paraphernalia or accessories, unless licensed and authorized by the jurisdiction in which the User is based as well as by the jurisdiction in which the transaction takes place;
* gambling activities including but not limited to sports betting, casino games, horse racing, dog racing, games that may be classified as gambling (i.e. poker), or other activities that facilitate any of the foregoing, unless licensed and authorized by the jurisdiction in which the User is based as well as by the jurisdiction in which the transaction takes place;
* money-laundering or terrorist financing;
* any sort of Ponzi scheme, pyramid scheme, or multi-level marketing program;
* goods or services that infringe or violate any copyright, trademark, or proprietary rights under the laws of any jurisdiction;
* credit repair services, or other services that may present consumer protection risks;
* court ordered payments, structured settlements, tax payments, or tax settlements;
* any unlicensed money transmitter activity;
* layaway systems, or annuities;
* counterfeit goods, including but not limited to fake or “novelty” IDs;
* wash trading, front-running, insider trading, market manipulation or other forms of market-based fraud or deceit;
* purchasing goods of any type from “Darknet” markets, or any other service or website that acts as a marketplace for illegal goods (even though such marketplace might also sell legal goods); or
* any other matters, goods, or services that from time to time we communicate to you that are unacceptable and which, for example, may be restricted by our and your bank or payment partners (such transactions, “Prohibited Transactions”).

In the event that Ethena BVI learns you are making any such Prohibited Transactions, Ethena BVI will consider you to be a violation of these Terms and may also suspend or terminate your status as a Mint User.

**18. Taxes**

The following only applies to Mint Users: Ethena BVI will maintain a record of your transaction history pursuant to the terms of the USDe Mint User Agreement. This transaction history will include all transactions you complete with Ethena BVI including tokenizing assets for USDe and redeeming USDe for assets.

**19. Indemnification; Release**

The following only applies to Mint Users: Section 22 of the USDe Mint User Agreement is hereby incorporated into these Terms by reference and shall apply in all respects to these Terms and your use of USDe Services and our products and services as contemplated herein.

The following only applies to Holding Users: You agree to indemnify and hold Ethena BVI, its affiliates, and service providers, and each of their officers, directors, agents, joint venturers, employees, and representatives harmless from any claim or demand (including attorneys’ fees and any losses, fines, fees or penalties imposed by any regulatory authority) arising out of your breach of these Terms, your violation of any law or regulation or your holding or use of USDe.

For the purpose of this Section 19, the term “losses” means all net costs reasonably incurred by us or the other persons referred to in this Section which are the result of the matters set out in this Section 19 and which may relate to any claims, demands, causes of action, debt, cost, expense or other liability, including reasonable legal fees (without duplication).

If you have a dispute with one or more Mint Users, Holding Users or third parties, you release Ethena BVI (and its affiliates and service providers, and each of their officers, directors, agents, joint ventures, employees and representatives) from all claims, demands, and damages (actual and consequential) of every kind and nature arising out of or in any way connected with such disputes.

**20. Limitation of Liability; No Warranty**

The following only applies to Mint Users: Section 23 of the USDe Mint User Agreement is hereby incorporated into these Terms by reference and shall apply in all respects to these Terms and your use of USDe Services and our products and services as contemplated herein.

The following only applies to Holding Users: YOU EXPRESSLY UNDERSTAND AND AGREE THAT Ethena BVI AND OUR AFFILIATES AND SERVICE PROVIDERS, AND THEIR RESPECTIVE OFFICERS, DIRECTORS, AGENTS, JOINT VENTURERS, EMPLOYEES, AND REPRESENTATIVES WILL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, EXEMPLARY DAMAGES, OR DAMAGES FOR LOSS OF PROFITS INCLUDING BUT NOT LIMITED TO, DAMAGES FOR LOSS OF GOODWILL, USE, DATA, OR OTHER INTANGIBLE LOSSES (EVEN IF Ethena BVI HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES), WHETHER BASED ON CONTRACT, TORT, NEGLIGENCE, STRICT LIABILITY, OR OTHERWISE, RESULTING FROM: (I) THE USE OR THE INABILITY TO HOLD OR USE USDe; (II) THE COST OF PROCUREMENT OF SUBSTITUTE GOODS AND SERVICES RESULTING FROM ANY GOODS, DATA, INFORMATION, OR SERVICES PURCHASED OR OBTAINED OR MESSAGES RECEIVED OR TRANSACTIONS ENTERED INTO INVOLVING USDe; (III) UNAUTHORIZED ACCESS TO OR ALTERATION OF YOUR TRANSMISSIONS OR DATA; OR (IV) ANY OTHER MATTER INVOLVING USDe.

SOME JURISDICTIONS DO NOT ALLOW THE EXCLUSION OF CERTAIN WARRANTIES OR THE LIMITATION OR EXCLUSION OF LIABILITY FOR INCIDENTAL OR CONSEQUENTIAL DAMAGES. ACCORDINGLY, SOME OF THE LIMITATIONS SET FORTH ABOVE MAY NOT APPLY TO YOU. IF YOU ARE DISSATISFIED WITH USDe, YOUR SOLE AND EXCLUSIVE REMEDY IS TO DISCONTINUE HOLDING AND USE OF USDe.

USDe IS PROVIDED "AS IS" AND WITHOUT ANY REPRESENTATION OR WARRANTY, WHETHER EXPRESS, IMPLIED OR STATUTORY. Ethena BVI, OUR AFFILIATES, AND OUR RESPECTIVE OFFICERS, DIRECTORS, AGENTS, JOINT VENTURERS,EMPLOYEES, AND SUPPLIERS SPECIFICALLY DISCLAIM ANY IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE OR NON-INFRINGEMENT. Ethena BVI MAKES NO WARRANTY THAT (I) USDeWILL MEET YOUR REQUIREMENTS, (II) USDe WILL BE UNINTERRUPTED, TIMELY, SECURE, OR ERROR-FREE, OR (III) THE QUALITY OF ANY PRODUCTS, SERVICES, INFORMATION, OR OTHER MATERIAL PURCHASED OR OBTAINED BY YOU WILL MEET YOUR EXPECTATIONS.

**21. Force Majeure**

Ethena BVI shall have no liability for any failure or delay resulting from any condition beyond our reasonable control, including but not limited to governmental action or acts of terrorism, earthquake, fire, flood, or other acts of God, labor conditions, power failures, equipment failures, and Internet disturbances.

**22. Amendments**

Ethena BVI may amend any portion of these Terms at any time by posting the revised version of these Terms with an updated revision date. The changes will become effective, and shall be deemed accepted by you, the first time you access or use USDe or the USDe Services after the initial posting of the revised Terms and shall apply on a going-forward basis with respect to transactions initiated after the posting date. In the event that you do not agree with any such modification, your sole and exclusive remedy is to terminate your use of the USDe Services and terminate your status as a Mint User (if any). You agree that we shall not be liable to you or any third party as a result of any losses suffered by any modification or amendment of these Terms.

If the revised Terms include a material change, we will provide you with prior notice via our website and/or email before the material change becomes effective. For this purpose a “material change” means a significant change other than changes that (i) are to your benefit, (ii) are required to be made to comply with applicable laws and/or regulations or as otherwise required by one of our regulators, (iii) relates to a new product or service made available to you, or (iv) otherwise clarifies an existing term.

**23. Assignment and Third-Party Holders**

You may not transfer or assign these Terms or any rights or obligations hereunder, by operation of law or otherwise and any such attempted assignment shall be void, subject to the following exception. Sending USDe to an address will automatically transfer and assign to that Holder, and any subsequent Holder, the right to redeem USDe for USD so long as the Holder is eligible to, and does, register as a Mint User.

Each Holding User is subject to all terms of these Terms as if a user including, but not limited to, the requirements to not transact with Blocked Addresses and not engage in Restricted Activities or Prohibited Transactions.

We reserve the right to freely assign these Terms and the rights and obligations of these Terms to any third party at any time without notice or consent. If you object to such transfer or assignment, you may stop holding and using USDe; further if you are a Mint User, you may also stop using our USDe Services, and terminate these Terms by contacting Support and asking us to terminate your status as a Mint User.

**24. Survival**

Upon termination of these Terms (and termination of your status as a Mint User, if you are a Mint User), all rights and obligations of the parties that by their nature are continuing will survive such termination.

**25. Website; Third Party Content**

Ethena BVI strives to provide accurate and reliable information and content on the Ethena BVI website, but such information may not always be correct, complete, or up to date. Ethena BVI will update the information on the Ethena BVI website as necessary to provide you with the most up to date information, but you should always independently verify such information. The Ethena BVI website may also contain links to third-party websites, applications, events or other materials (“Third Party Content”). Such information is provided for your convenience and links or references to Third Party Content do not constitute an endorsement by Ethena BVI of any products or services. Ethena BVI shall have no liability for any losses incurred as a result of actions taken in reliance on the information contained on the Ethena BVI website or in any Third Party Content.

**26. Governing Law; Venue**

The laws of the British Virgin Islands shall govern these Terms. The courts of the British Virgin Islands shall have exclusive jurisdiction to settle any dispute arising out of, or connected with, these Terms.

**27. Entire Agreement**

The following applies to both Mint Users and Holding Users: The failure of Ethena BVI to exercise or enforce any right or provision of these Terms shall not constitute a waiver of such right or provision. If any provision of these Terms shall be adjudged by any court of competent jurisdiction to be unenforceable or invalid, that provision shall be limited or eliminated to the minimum extent necessary so that these Terms shall otherwise remain in full force and effect and remain enforceable between the parties, except as specified in Section 27. Furthermore, if any portion of these Terms, whether in whole, or in part, shall be adjudged by any court of competent jurisdiction to be unenforceable or invalid against certain persons or categories of persons that are purportedly bound by these Terms, such portion of these Terms shall otherwise remain in full force and effect and remain enforceable as to any other persons bound by these terms. The headings and explanatory text are for reference purposes only and in no way define, limit, construe, or describe the scope or extent of such section. These Terms, the USDe Mint User Agreement, the General Terms of Service, and Ethena BVI’s policies governing the holding or use of USDe, the use of the USDe Services referenced herein, and the Privacy Policy t constitute the entire agreement between you and Ethena BVI with respect to the holding or use of USDe, and the use of the USDe Services. These Terms are not intended and shall not be construed to create any rights or remedies in any parties other than you and Ethena BVI and other Ethena BVI affiliates which each shall be a third-party beneficiary of these Terms, and no other person shall assert any rights as a third-party beneficiary hereunder.

The following only applies to Mint Users: Notwithstanding anything to the contrary set forth in these Terms or otherwise, in the event of a conflict between any term set forth herein and any term set forth in the USDe Mint User Agreement (i) in connection with any USDe transaction, the terms of these Terms shall control, and (ii) in respect of any other Digital Currency transaction, the terms of the USDe Mint User Agreement shall control.

**28. E-Sign Consent**

Please be aware that your consent to the electronic delivery of disclosures is required to use any of the Services (as defined in the USDe Mint User Agreement). If you are unable or unwilling to provide such consent, you will not be able to become a Mint User. Once you are a Mint User you can rescind your consent to electronic delivery of disclosures at any time and receive paper communications as set forth below.

This E-Sign Consent applies to any and all communications and/or disclosures that Ethena BVI is legally required to provide to you in writing in connection with your status as a Mint User and any related products and services (“Communications”). This E-Sign Consent supplements and is to be construed in accordance with the terms and conditions contained in the USDe Mint User Agreement.

When you use the Services, you agree that we may provide you with any Communications in electronic format, and that we may discontinue sending paper Communications to you, unless and until you withdraw your consent as described below. Your consent to receive electronic communications and transactions includes, but is not limited to:

* Legal and regulatory disclosures and communications associated with your registration or the Services;
* Notices or amendments relating to the USDe Mint, User Agreement, the Privacy Policy, the Cookie Policy or this E-Sign Consent;
* Communications regarding any transactions; and
* Responses to claims filed in connection with your relationships with Ethena BVI as a Mint User.

Methods of Communication

All Communications that we provide to you in electronic form will be provided by e-mail, by posting to the Ethena BVI website (USDe.money), or through other electronic communication such as mobile push notification or text message.

Hardware Requirements

In order to access, view, and retain electronic Communications that we make available to you, you must have the following software and hardware:

* A valid e-mail address.
* A computer or other device capable of accessing the internet with a current web browser that supports at least 128 bit encryption, such as Google Chrome, Apple® Safari, Microsoft® Internet Explorer, or Mozilla Firefox®. The browser must have cookies enabled.
* The computer must also have a printer or disk drive to print or retain copies of this E-Sign Consent and any Communications.

Updating your Information

It is your responsibility to provide us with a true, accurate and complete e-mail address, your contact information, and other information related to this E-Sign Consent and your registration, keep such information up to date.

Withdrawing Consent

You may withdraw your consent to receive electronic Communications at any time by sending us a written request by email. You understand that any withdrawal of your consent to receive electronic Communications will be effective only after Ethena BVI has had a reasonable period of time to process your withdrawal. You understand that withdrawing your consent to electronic Communications will likely result in the termination of your status as a Mint User.

Communications in Writing

All electronic Communications from us to you will be considered "in writing" and shall have the same meaning and effect as a paper Communication. You should print or download for your records a copy of this E-Sign Consent and any other Communication that is important to you. You acknowledge and agree that Communications are considered received by you within 24 hours of the time posted to the Ethena BVI website (USDe.money), or within 24 hours of the time emailed to you unless Ethena BVI receives notice that the email was not delivered.

General

Ethena BVI reserves the right, in our sole discretion, to cancel this electronic Communication service, or to terminate or change the terms and conditions on which Ethena BVI provides electronic Communications. Ethena BVI will provide you with notice of any such termination or change as required by law.

Last updated 4 months ago

Was this helpful?

---


# USDe Mint User Agreement - Non EEA

Source: https://docs.ethena.fi/resources/usde-mint-user-agreement-non-eea

Last Updated: January 2025

This USDe Mint User Agreement (this “Agreement”) is a contract between you (“you” or a “ Mint User”) and Ethena BVI Limited ("referred to as the “Company,” and “Ethena BVI”, “we,” or “us”)If you are a user outside the EEA, this Agreement applies to your use of Ethena BVI--related products and services (the “Services”) on the Company platform (the “Platform” or “Company”). The USDe Terms apply to your USDe and your status as a Mint User, as applicable, as defined in the USDe Terms. From and after the date set forth above, this Agreement shall govern your use of any Company products or Services.

For the avoidance of doubt, your access to the Services is contingent on your status as a Mint User, as defined herein.

By registering as a Mint User or using any of the Services, you agree that you have read, understood and accept all of the terms and conditions contained in this Agreement as well as the Privacy Policy, Cookie Policy, and other policies, and you acknowledge and agree that you will be bound by these agreements and policies.

Note that this Agreement uses the term “Digital Currency” to refer to USDe or any other digital currencies, cryptocurrencies, virtual currencies, or digital assets. For the avoidance of doubt, where used herein, the term “funds” includes Digital Currency.

Please note that Section 20 contains an arbitration clause and collective or class action waiver. By agreeing to this Agreement, you agree to resolve all disputes, except as otherwise set forth in Section 20, through binding individual arbitration, which means that you waive any right to have the dispute decided by a judge or jury, and you waive any right to participate in collective action, whether that be a class action, class arbitration, or representative action.

Section 21 of this Agreement governs how this Agreement may be changed over time; the date of the last update is set forth at the top of this Agreement.

**1. Eligibility; Limitations; Registration Process; Identity Verification**

Eligibility; Limitations

The Platform and the Services are currently only available to users located in supported jurisdictions. In registering to use the Company Services as a Mint User on behalf of an entity, you represent and warrant that (i) such legal entity is duly organized and validly existing under the applicable laws of the jurisdiction of its organization; (ii) you are duly authorized by such legal entity to act on its behalf, and (iii) such organization (and any affiliate entity) must not have been previously suspended or removed from the Services or any other service or product offered by the Company or its affiliate entities.

Use of certain Services may have further eligibility requirements that will need to be verified prior to you using such Services or from time to time in order to continue your use of the Services and may be subject to additional terms and conditions.

By using your status as a Mint User and the Services, you further represent and warrant that:

* you are at least 18 years old and are not a Restricted Person, nor are you resident of a Restricted Territory (each as defined in Section 27 below).
* you will not be using your status as a Mint User and Services for any illegal activity, including, but not limited to, illegal gambling, money laundering, fraud, blackmail, extortion, ransoming data, terrorism financing, other violent activities or any prohibited market practices, including, but not limited to, those listed in the USDe Terms and Conditions.

You also understand that there are additional representations and warranties made by you elsewhere in (or by reference in) this Agreement and that any misrepresentation by you is a violation of this Agreement.

Users in the United States are not eligible to become a Mint User. This restriction may be revisited from time to time taking into account relevant changes in law.

When you register as a Mint User, you will be required to designate an administrator for your registration and provide a wallet address to be whitelisted. The Company may, in its discretion, enable functionality utilizing your status as a Mint User and some or all of the Services to other persons at your firm (e.g. your employees) (such persons, “Additional Users”). Such access is subject to the Company’s review and approval, and such Additional Users’ agreement to all of the terms hereof. To the extent that you choose to have Additional Users have access and control over the Mint User profile and relationship, you will have to designate those Additional Users and manage their access to your Mint User whitelisted wallets. By you requesting such access, you and all Additional Users automatically agree to this Agreement.

If the Company determines that you or any of your Additional Users have violated this Agreement, including, but not limited to, transacting with Blocked Addresses (as defined in the USDe Terms and Conditions) or engaging in Restricted Activities or Prohibited Transactions then the Company may be forced to terminate your status as a Mint User.

Notwithstanding the foregoing, the Company may determine not to make the Services, in whole or in part, available in every market, either in its sole discretion or due to legal or regulatory requirements, depending on your location. We may also, without liability to you or any third party, refuse to let you register as a Mint User in the Company’s sole discretion.

Registration Process; Identity Verification

When registering as a Mint User, you must provide current, complete, and accurate information for all required elements on the registration page or via any third-party service providers (e.g., KYC/KYB information collection and screening providers), including your full legal name and the legal name of your organization. You also agree to provide us, when registering as a Mint User and on an ongoing basis, any additional information we request for the purposes of identity verification and the detection of money laundering, terrorist financing, fraud, or any other financial crime. You permit us to keep a record of such information and authorize us to make the inquiries, whether directly or through third parties, that we consider necessary or desirable to verify your identity or protect you and/or us against fraud or other financial crime, and to take action we reasonably deem necessary based on the results of such inquiries. When we carry out these inquiries, you understand, acknowledge and agree that your personal information may be disclosed to credit reference and fraud prevention or financial crime agencies and that these agencies may respond to our inquiries in full.

In certain circumstances, we may require you to submit additional information about yourself or your business, provide records, and complete other verification steps (such process, "Enhanced Due Diligence").

You represent and warrant that all information provided to us pursuant to this Agreement is true, accurate and not misleading in any respect. If any such information changes, it is your obligation to update such information as soon as possible.

From time to time we may be required to request further information or review or update existing information regarding your registration or your transactions to comply with applicable laws and regulation, and in some cases, payment network. Failure to provide such information, if requested by the Company, in a timely fashion may result in the suspension of your ability to use the Services (until you provide such information) or the termination of your status as a Mint User.

We reserve the right to maintain your registration information after you terminate your status as a Mint User for business and regulatory compliance purposes, subject to applicable laws and regulation.

**2. Services**

The Company offers the following Services in connection with your status as a Mint User:

The Company provides USDe-related services, which are described more fully in Section 10 and in the USDe Terms. The USDe Terms are incorporated herein by reference.

**3. Custody**

The Company does not provide any custody services with respect to USDe or any other assets. Additionally, for the avoidance of doubt, the Company is not a fiduciary, and the Company does not provide any trust or fiduciary services to any User in the course of such User visiting, accessing, or using the the Company website or services, including, for the avoidance of doubt, holding USDe.

Legal title to the reserves associated with USDe are held by the Company, which administers the assets accordingly. Ultimate economic ownership of the reserves inures to the Ethena Foundation, an independent third party formed for the purpose of supporting the Ethena Protocol and its architecture. 

**4. No Investment Advice**

The Company does not provide investment, tax, or legal advice, nor does the Company broker trades on your behalf. You should consult your legal or tax professional regarding your specific situation. The Company may provide educational information about USDe and other Digital Currency not supported by the Company. Information may include, but is not limited to, blog posts, articles, links to third-party content, news feeds, tutorials, and videos. The information provided on this website or any third-party sites does not constitute investment advice, financial advice, trading advice, or any other sort of advice, and you should not treat any of the website's content as such.

**5. Privacy**

We are committed to protecting your personal information and helping you understand exactly how your personal information is being used. You should carefully read the Privacy Policy as it provides details on how your personal information is collected, stored, protected, and used.

**6. Communications**

By entering into this Agreement, you agree to receive electronic communications and notifications in accordance with our E-Sign Consent Policy, as detailed in the USDe Terms.

This Agreement is provided to you and communicated in English. We will also communicate with you in English for all matters related to your use of the Services. Where we have provided you with a translation of the English language version of this Agreement or any information related to your status as a Mint User, you acknowledge and agree that such translation is provided for your convenience only and that the English language version of the Agreement will govern your use of the Services.

**7. Security of User Information**

You are responsible for maintaining the confidentiality and security of all account names, User IDs, passwords, seed phrases, private keys, personal identification numbers (PINs) and other access codes that you use to access the Services. You are responsible for keeping your email address and all other access and User information up to date with us and for maintaining the confidentiality of your User information. You agree to (i) notify the Company immediately if you become aware of any unauthorized use of your registration as a Mint User, the Services, or any other breach of security regarding the Services or the Platform. We strongly advise you to enable all security features that are available to you (such as, by way of example, using hardware wallets to secure private keys); this offers you enhanced protection from possible malicious attacks. The Company will not be liable for any loss or damage arising from your failure to protect your registration information or private keys.

We shall not bear any liability for any damage or interruptions caused by any computer viruses, spyware, or other malware that may affect your computer or other equipment, or any phishing, spoofing, or other attack. We recommend the regular use of a reliable virus and malware screening and prevention software. If you question the authenticity of a communication purporting to be from the Company, you should contact a representative directly.

**8. Suspension & Closure**

We may, without liability to you or any third party, suspend your status as a Mint User or terminate your status as a Mint User or suspend your use of one or more of the Services in accordance with the terms of this Agreement, as determined in our sole and absolute discretion. Such actions may be taken as a result of inactivity, failure to respond to customer support requests, failure to positively identify you, a court order, your violation of the terms of this Agreement or for other similar reasons. The Company may also temporarily suspend your status as a Mint User in the event that a technical problem causes system outage or the Company errors until the problem is resolved. For the avoidance of doubt, in the event your status as a Mint User is suspended or closed, you will no longer be able to access any of the Services.

You may terminate this Agreement at any time by terminating your status as a Mint User in accordance with this Agreement. In order to do so, you should contact the Company’s “Support Team” who will assist you in terminating your status as a Mint User. You may not terminate your status as a Mint User if the Company believes, in its sole discretion, that such termination is being performed in an effort to evade a court order or legal or regulatory investigation or to avoid paying any amounts otherwise due to the Company.

Upon closure or suspension of your status as a Mint User, you authorize the Company to cancel or suspend pending transactions and forfeit all proprietary rights and claims against the Company in relation to any assets otherwise eligible for redemption.

In the event that you or the Company terminates this Agreement or your access to the Services, or cancels your status as a Mint User, you remain liable for all activity conducted on or with your status as a Mint User while it was active and for all amounts due hereunder.

**9. Fees**

The Company may charge fees in connection with the Services, which will typically not represent fees for the Company’s own account and will constitute reimbursements for costs associated with transactions initiated by you, such as blockchain gas fees and execution fees. You agree to pay the fees shown to you, if any, or as separately agreed between you and the Company, when you enter into a transaction. Fees are generally disclosed prior to your confirmation of any transaction with the Company; we may change any of the fees that the Company charges at any time, with or without notice.

The applicable Digital Currency network may charge a fee in connection with blockchain transactions. You are responsible for all such fees.

**10. Applicable USDe Terms**

To the extent that you utilize your status as a Mint User for any transaction or service involving USDe to which the Company is a counterparty, the USDe Terms shall apply to all such transactions and such agreement. Notwithstanding anything to the contrary set forth in this Agreement or otherwise, in the event of a conflict between any term set forth herein and any term set forth in the USDe Terms, (i) in connection with any USDe transaction, the terms of the USDe Terms shall control, and (ii) in respect of any other Digital Currency transaction, the terms of this Agreement shall control.

**11. Mobile Services**

To the extent you access the Services through a mobile device, your wireless service carrier’s standard charges, data rates, and other fees may apply. In addition, downloading, installing, or using certain mobile applications may be prohibited or restricted by your carrier, and not all Services may work with all carriers or devices. By using mobile Services, you agree that we may communicate with you by SMS, MMS, text message, push notification, and/or other electronic means via your mobile device (“Mobile Messaging”) and that certain information about your usage of the Services may be communicated to us. In the event that you change or deactivate your mobile telephone number, you agree to promptly update your registration information to ensure that your messages are not sent to any person who might acquire your old number.

You may receive messages related to the Services or your status as a Mint User via Mobile Messaging. Message and data rates may apply. Reply STOP to any such Mobile Message to Cancel and unsubscribe. For help, please contact the Support Team.

You hereby confirm that with respect to any mobile phone number provided, you own the account corresponding to that mobile phone number or otherwise have the account holder’s permissions to use this service. By registering a mobile phone number you are agreeing to the specific terms set forth in this Section 11.

**12. Transaction Limits**

The Company reserves the right to change the mint, redemption, transfer, and velocity limits as we deem necessary. We may establish individual or aggregate transaction limits on the size or number of mints, redemptions, transfers or other transactions that you initiate using your status as a Mint User during any specified time period.

**13. Right to Change/Remove Features or Suspend/Delay Transactions**

Subject to Section 17 of the USDe Terms, we reserve the right to change, suspend, or discontinue any aspect of the Services or the Platform at any time, including hours of operation or availability of any feature, without notice and without liability. We may, in our sole discretion, delay any transaction if we believe that such transaction is suspicious, may involve fraud or misconduct, violates applicable laws or payment network rules, or violates any term of this Agreement.

**14. Insufficient Funds**

If you have insufficient funds in your whitelisted wallet associated with your status as a Mint User to complete a transaction, such transaction will not be completed.

**15. Refunds; Reversals**

Once a transaction has been initiated (including, but not limited to, a Digital Currency Transfer), it cannot be reversed or refunded, except as set forth in this Agreement. You may have additional refund or chargeback rights under your agreement with the recipient of such funds, your financial institution, or applicable law. You should periodically review statements from your financial institution and any other service that you use to transact Digital Currency, which should reflect all applicable transactions made using the related transaction method.

**16. Taxes**

It is your responsibility to determine what, if any, taxes apply to the payments you make or receive, and to collect, report, and remit the correct tax to the appropriate tax authority. the Company is not responsible for determining whether taxes apply to your transaction, or for collecting, reporting, or remitting any taxes arising from any transaction.

**17. Indemnification; Release**

You agree to indemnify and hold the Company, its affiliates, and service providers, and each of their officers, directors, agents, joint venturers, employees, and representatives harmless from any claim or demand (including attorneys’ fees and any losses, fines, fees or penalties imposed by any regulatory authority) arising out of your breach of this Agreement, your violation of any law or regulation or your use of the Services.

For the purpose of this Section 17, the term “losses” means all net costs reasonably incurred by us or the other persons referred to in this Section which are the result of the matters set out in this Section 19 and which may relate to any claims, demands, causes of action, debt, cost, expense or other liability, including reasonable legal fees (without duplication).

If you have a dispute with one or more Users or third parties, you release the Company (and its affiliates and service providers, and each of their officers, directors, agents, joint ventures, employees and representatives) from all claims, demands, and damages (actual and consequential) of every kind and nature arising out of or in any way connected with such disputes.

**18. Limitation of Liability; No Warranty**

YOU EXPRESSLY UNDERSTAND AND AGREE THAT THE COMPANY AND OUR AFFILIATES AND SERVICE PROVIDERS, AND THEIR RESPECTIVE OFFICERS, DIRECTORS, AGENTS, JOINT VENTURERS, EMPLOYEES, AND REPRESENTATIVES WILLNOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, EXEMPLARY DAMAGES, OR DAMAGES FOR LOSS OF PROFITS INCLUDING BUT NOT LIMITED TO, DAMAGES FOR LOSS OF GOODWILL, USE, DATA, OR OTHER INTANGIBLE LOSSES (EVEN IF THE COMPANY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES),WHETHER BASED ON CONTRACT, TORT, NEGLIGENCE, STRICT LIABILITY, OR OTHERWISE, RESULTING FROM: (I) THE USE OR THE INABILITY TO USE THE SERVICES; (II) THE COST OF PROCUREMENT OF SUBSTITUTE GOODS AND SERVICES RESULTING FROM ANY GOODS, DATA, INFORMATION, OR SERVICES PURCHASED OR OBTAINED OR MESSAGES RECEIVED OR TRANSACTIONS ENTERED INTO THROUGH OR FROM THE SERVICES; (III) UNAUTHORIZED ACCESS TO OR ALTERATION OF YOUR TRANSMISSIONS OR DATA; OR (IV) ANY OTHER MATTER RELATING TO THE SERVICES.

SOME JURISDICTIONS DO NOT ALLOW THE EXCLUSION OF CERTAIN WARRANTIES OR THE LIMITATION OR EXCLUSION OF LIABILITY FOR INCIDENTAL OR CONSEQUENTIAL DAMAGES. ACCORDINGLY, SOME OF THE LIMITATIONS SET FORTH ABOVE MAY NOT APPLY TO YOU. IF ANY PROVISION OF THIS SECTION CANNOT BE GIVEN FULL EFFECT UNDER THE LAWS OF YOUR JURISDICTION, REVIEWING COURTS SHALL APPLY LOCAL LAW THAT MOST CLOSELY APPROXIMATES THE INTENDED ECONOMIC EFFECT OF SUCH PROVISION, INCLUDING AN ABSOLUTE WAIVER OF ALL CIVIL LIABILITY IN CONNECTION WITH THE SERVICES TO THE EXTENT PERMITTED BY LAW. IF YOU ARE DISSATISFIED WITH ANY PORTION OF THE SERVICES OR WITH THIS AGREEMENT, YOUR SOLE AND EXCLUSIVE REMEDY IS TO DISCONTINUE USE OF THE SERVICES AND TERMINATE YOUR STATUS AS A MINT USER.

THE SERVICES ARE PROVIDED "AS IS" AND WITHOUT ANY REPRESENTATION OR WARRANTY, WHETHER EXPRESS,IMPLIED OR STATUTORY. THE COMPANY, OUR AFFILIATES, AND OUR RESPECTIVE OFFICERS, DIRECTORS, AGENTS, JOINT VENTURERS, EMPLOYEES, AND SUPPLIERS SPECIFICALLY DISCLAIM ANY IMPLIED WARRANTIES OF TITLE,MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE OR NON-INFRINGEMENT. THE COMPANY MAKES NO WARRANTY THAT (I) THE SERVICES WILL MEET YOUR REQUIREMENTS, (II) THE SERVICES WILL BE UNINTERRUPTED, TIMELY, SECURE, OR ERROR-FREE, OR (III) THE QUALITY OF ANY PRODUCTS, SERVICES, INFORMATION, OR OTHER MATERIAL PURCHASED OR OBTAINED BY YOU WILL MEET YOUR EXPECTATIONS.

The Company will make reasonable efforts to ensure that requests for the Company transactions are processed in a timely manner, but the Company makes no representations or warranties regarding the amount of time needed to complete processing because the Services are dependent upon many factors outside of our control, such as delays in the banking system. or international mail service. Some jurisdictions do not allow the disclaimer of implied warranties, so the foregoing disclaimers may not apply to you. This Section gives you specific legal rights and you may also have other legal rights that vary from state to state.

**19. Right to Set Off**

The Company may and is authorized, without prior notice and both before and after demand, to set off the whole or any part of your liabilities or other amounts payable to the Company, including but not limited to fees, whether such amounts are present or future, actual or contingent, or liquidated or unliquidated, against any sums held by the Company and owed to you, whether under this Agreement or any other agreement between the Company and you.

For the purpose of exercising its rights under this Section 21: (i) the Company is entitled to convert and/or exchange any Supported Digital Currency owned by you and held by the Company, and is authorized to effect any such conversions at the then prevailing exchange rate; and (ii) if your liability is contingent and/or unliquidated, then the Company may set off the amount it estimates in good faith will be the liquidated amount.

**20. Arbitration**

Except for claims for injunctive or equitable relief or claims regarding intellectual property rights (which may be brought, in an individual capacity only, and not on a class-wide or representative basis, in the courts specified in Section 28 without the posting of a bond), any dispute between you and the Company related in any way to, or arising in any way from, our Services or this Agreement (“Dispute”) shall be finally settled on an individual, non-representative basis in binding arbitration shall be settled by arbitration in accordance with the BVI IAC Arbitration Rules, as modified by this Agreement, or in accordance with rules on which we may mutually agree in writing; provided, however, that to the extent a Dispute is within the scope of a small claims court’s jurisdiction, either you or the Company may commence an action in small claims court, in the county of your most recent physical address, to resolve the Dispute.

Any arbitration will be conducted by a single, neutral arbitrator and shall take place in Road Town, Tortola, British Virgin Islands, unless we agree otherwise. The arbitrator may award any relief that a court of competent jurisdiction could award, including attorneys’ fees when authorized by law. The arbitral decision may be enforced in any court of competent jurisdiction. An arbitral decision is subject to very limited review by a court.

**21. Amendments**

The Company may amend any portion of this Agreement at any time by posting the revised version of this Agreement with an updated revision date. The changes will become effective, and shall be deemed accepted by you, the first time you use the Services after the initial posting of the revised Agreement and shall apply on a going-forward basis with respect to transactions initiated after the posting date. In the event that you do not agree with any such modification, your sole and exclusive remedy is to terminate your use of the Services and terminate your status as a Mint User. You agree that we shall not be liable to you or any third party as a result of any losses suffered by any modification or amendment of this Agreement.

If the revised Agreement includes a material change, we will provide you with prior notice via our website and/or email before the material change becomes effective. For this purpose a “material change” means a significant change other than changes that (i) are to your benefit, (ii) are required to be made (a) to comply with applicable laws and/or regulations, (b) to comply with a payment network , or (c) as otherwise required by one of our regulators, (iii) relates to a new product or service made available to you, or (iv) to otherwise clarify an existing term.

**22. Assignment**

You may not transfer or assign this Agreement or any rights or obligations hereunder, by operation of law or otherwise and any such attempted assignment shall be void. We reserve the right to freely assign this Agreement and the rights and obligations of this Agreement to any third party at any time without notice or consent. If you object to such transfer or assignment, you may stop using our Services and terminate this Agreement by contacting the Company’s Support Team and asking us to terminate your status as a Mint User.

**23. Change of Control**

In the event that the Company is acquired by or merged with a third party entity, we reserve the right, in any of these circumstances, to transfer or assign the information we have collected from you as part of such merger, acquisition, sale, or other change of control.

**24. Survival; Force Majeure**

Upon termination of your status as a Mint User or this Agreement for any reason, all rights and obligations of the parties that by their nature are continuing will survive such termination.

The Company shall have no liability for any failure or delay resulting from any condition beyond our reasonable control, including but not limited to governmental action or acts of terrorism, pandemics, earthquake, fire, flood, or other acts of God, labor conditions, power failures, equipment failures, and Internet disturbances.

**25. Website; Third Party Content**

The Company strives to provide accurate and reliable information and content on the Company website, but such information may not always be correct, complete, or up to date. The Company will update the information on the Company website as necessary to provide you with the most up to date information, but you should always independently verify such information. The Company website may also contain links to third party websites, applications, events or other materials (“Third Party Content”). Such information is provided for your convenience and links or references to Third Party Content do not constitute an endorsement by the Company of any products or services. The Company shall have no liability for any losses incurred as a result of actions taken in reliance on the information contained on the Company website or in any Third Party Content.

**26. Limited License; IP Rights**

We grant you a limited, non-exclusive, non-sublicensable, and non-transferable license, subject to the terms and conditions of this Agreement, to access and use the Services solely for approved purposes as determined by the Company. Any other use of the Services or the Platform is expressly prohibited. the Company and its licensors reserve all rights in the Services and you agree that this Agreement does not grant you any rights in or licenses to the Services except for the limited license set forth above. Except as expressly authorized by the Company, you agree not to modify, reverse engineer, copy, frame, scrape, rent, lease, loan, sell, distribute, or create derivative works based on the Services or the Platform, in whole or in part. If you violate any portion of this Agreement, your permission to access and use the Services and your status as a Mint User may be terminated pursuant to this Agreement. "USDe.money", "the Company", and all logos related to the Services are either trademarks, or registered marks of the Company or its licensors. You may not copy, imitate, or use them without the Company's prior written consent. All right, title, and interest in and to the the Company website, any content thereon, the Services, and all technology and any content created or derived from any of the foregoing is the exclusive property of the Company and its licensors.

**27. Applicable Law; Legal Compliance**

Your use of the Services is subject to the laws, regulations, and rules of any applicable governmental or regulatory authority, including, without limitation, all applicable tax, anti-money laundering (“AML”) and counter-terrorist financing (“CTF”) provisions.

You unequivocally agree and understand that by registering as a Mint User and using the Services in any capacity, you will act in compliance with and be legally bound by this Agreement and all applicable laws and regulations (including, without limitation, those stated in this Section 27, where applicable). For the avoidance of doubt, continued use of your status as a Mint User and the Company’s obligations to you under this Agreement are conditional on your continued compliance at all times with this Agreement and all applicable laws and regulations. The Company’s AML and CTF procedures are guided by all applicable laws and regulations regarding AML and CTF. These standards are designed to prevent the use of the Services for money laundering or terrorist financing activities. We take compliance very seriously and it is our policy to take all necessary steps to prohibit fraudulent transactions, report suspicious activities, and actively engage in the prevention of money laundering and any related acts that facilitate money laundering, terrorist financing or any other financial crimes.

You agree, represent, and warrant that all funds transacted as a Mint User, or funds deposited by you with the Company in the future, are not the direct or indirect proceeds of any criminal or fraudulent activity.

The Services are subject to economic sanctions programs administered in the countries where we conduct business, including but not limited to those administered by the U.S. Department of Treasury’s Office of Foreign Assets Control (“OFAC”), pursuant to which we are prohibited from providing services or entering into relationships with certain individuals and institutions. By using the Services, you represent that your actions are not in violation of such sanctions programs. Without limiting the foregoing, you may not use the Services if (i) you are a resident, national or agent of a jurisdiction subject to comprehensive sanctions by OFAC (“Restricted Territories”), (ii) you are on the Table of Denial Orders, the Entity List, or the List of Specially Designated Nationals (“Restricted Persons”), or (iii) you intend to transact with any Restricted Territories or Restricted Persons. You further represent that you are not a citizen, resident, or organized in, the following jurisdictions (the “Prohibited Jurisdictions”): Abkhazia, Afghanistan, Angola, Belarus, Burundi, Central African Republic, Congo, Cuba, Crimea, Ethiopia, Guinea-Bissau, Iran, Ivory Coast (Cote D’Ivoire), Lebanon, Liberia, Libya, Mali, Burma (Myanmar), Nicaragua, North Korea, Northern Cyprus, Russia, Somalia, Somaliland, South Ossetia, South Sudan, Sudan, Syria, Ukraine (Donetsk and Luhansk regions), United States, Venezuela, Yemen, Zimbabwe.

In the event that we are required to block funds associated with your registration as a Mint User in accordance with a sanctions program, or other similar government sanctions programs, we may: (i) suspend your status as a Mint User; (ii) terminate your status as a Mint User; or (iii) return funds to the destination of their origin or to an account specified by authorities. In certain cases, taking one or more of these actions may result in a forfeiture of some or all of your assets held with the Company. We are not responsible for any losses, whether direct or indirect, that you may incur as a result of our complying with applicable law and regulations, the guidance or direction of any regulatory authority or government agency, or any writ of attachment, lien, levy, subpoena, warrant, or other legal order.

**28. Governing Law; Venue**

The laws of the British Virgin Islands shall govern this Agreement. Except for those disputes that shall be resolved in arbitration or in small claims court, each party agrees to submit to the personal and exclusive jurisdiction of the courts located in the British Virgin Islands, provided that any claims or disputes shall be subject to the arbitration provisions set forth in Section 20. You agree with us that, if you are a consumer, the courts in the permitted region where you are resident will have non-exclusive jurisdiction.

**29. Entire Agreement**

The failure of the Company to exercise or enforce any right or provision of the Agreement shall not constitute a waiver of such right or provision. If any provision of this Agreement shall be adjudged by any court of competent jurisdiction to be unenforceable or invalid, that provision shall be limited or eliminated to the minimum extent necessary so that this Agreement shall otherwise remain in full force and effect and remain enforceable between the parties, except as specified in Section 25. The headings and explanatory text are for reference purposes only and in no way define, limit, construe, or describe the scope or extent of such section. This Agreement, including any additional agreement incorporated by reference herein; the Company’s policies governing the Services referenced herein (including, without limitation, those set forth in the USDe Terms); the the Company Privacy Policy and the Cookie Policy constitute the entire agreement between you and the Company with respect to the use of the Services. This Agreement is not intended and shall not be construed to create any rights or remedies in any parties other than you and the Company and other the Company affiliates which each shall be a third-party beneficiary of this Agreement, and no other person shall assert any rights as a third-party beneficiary hereunder.

**30. User Support**

Please contact our Support Team to report any violations of this Agreement or to ask any questions regarding this Agreement or the Services.

Last updated 4 months ago

Was this helpful?

---
