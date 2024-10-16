+++
title = "Big Picture"
description = ""
weight = 2
+++

Lokad is a programmatic, SaaS platform designed for Supply Chain Scientists to execute Quantitative Supply Chain initiatives. The present documentation has been created for a modestly technical audience - typically people who feel at ease writing spreadsheet formulas. Lokad is intended to be accessible to people who are not professional software engineers, but supply chain experts. Below, we provide a technical overview of Lokad, and an initial introduction to Envision, its Domain Specific programming Language (DSL).

**Table of contents**
{{< toc >}}{{< /toc >}}

## Motivated by Supply Chain

The [Quantitative Supply Chain](https://www.lokad.com/resources) represents a specific way of tackling Supply Chain Management (SCM) challenges, which Lokad has pioneered and refined over the years. Lokad adopts a broad perspective on SCM, as pricing and assortment decisions also fall under our SCM umbrella. Indeed, SCM is not only about “keeping up” with demand, but also shaping it whenever it is opportune or profitable.

Lokad is a _programmatic_ SaaS platform that has been engineered to craft, deliver and maintain _bespoke predictive optimization apps_ intended to execute Quantitative Supply Chain initiatives. In this respect, Lokad is quite unlike most enterprise apps. Lokad does not deliver an out of the box _solution_. Lokad provides the _capabilities_ to build a bespoke app that delivers the solution. This app can automatically process all relevant data and deliver both optimized results and the supporting dashboards. The app is written in a programming language named _Envision_, that has been engineered by Lokad. Unlike general purpose programming languages, Envision is accessible to non specialists, i.e. people who are not professional software engineers.

We refer to people who are capable of executing Quantitative Supply Chain initiatives as [Supply Chain Scientists](https://www.lokad.com/the-supply-chain-scientist). The goal of the present documentation is to provide the technical know-how related to Envision in order to execute such initiatives. Envision is heavily geared towards the resolution of common supply chain problems, however, the actual resolution of supply chain problems requires a fair amount of supply chain expertise before any kind of programming is performed. Actually, we believe that with proper tools, like Envision, supply chain expertise is by far the biggest challenge - not programming with Envision.

Lokad comes in two flavors: either pure software or software+experts. With our clients, we nearly always start with the software+experts flavor, where Lokad provides a team of Supply Chain Scientists _as a service_ on top of providing its SaaS (Software as a Service) platform. Over Lokad’s history, we realized early on that one of the most powerful ways of de-risking supply chain initiatives was to rely on experienced teams who had “already done it”. Fail fast and break things is typically not advised for supply chain undertakings.

Nevertheless, Lokad’s technical documentation is public and anyone can train to become a Supply Chain Scientist and Envision wizard. This documentation is used internally at Lokad to train our new Supply Chain Scientists to use our platform. It can also be used by client companies to train their own teams, and ultimately take over the management of their own predictive optimization apps. Beyond that, we also believe that this documentation is of interest to supply chain enthusiasts who have realized, like us, that most popular supply chain recipes, such as ABC analysis or safety stocks, are simply not _good enough_.

## The genesis of Envision

Envision was not part of our technology roadmap when Lokad was founded in 2008. It took us several years, from 2008 and 2013, and numerous unsuccessful attempts at alternative solutions to even start considering an undertaking as major as the creation of a Domain Specific programming Language (DSL). More specifically, the crux of the problem was our capacity to turn our promising prototypes intended for predictive supply chain optimization into production-grade solutions.

We were not alone in facing this problem. Back in 2012, while “data science” was not yet the buzzword it would become in the years that followed, we witnessed our most tech-driven clients - typically North American ecommerces - try hard and fail hard at bringing Python prototypes to production. Even when those solutions made it to production, maintenance was a nightmare. Since that time, newer and better machine learning algorithms have been uncovered but, for most supply chain situations, even back in 2012, machine learning was no longer the bottleneck. As Eliyahu M. Goldratt pointed out in his 1984 book entitled _The Goal_, improvements made anywhere besides the bottleneck are an illusion.

During 2014, as Lokad started its “dogfooding” process by using the first version of Envision for some of our internal projects, all geared toward flavors of supply chain optimization, it became clear that, Envision-powered initiatives were systemically outperforming the alternative initiatives carried out by generic programming languages, even with top-notch software developers.

We do not claim that Envision is better than Python/Java/C#/SQL/etc in the general case. Envision itself implemented using C#, F# and Typescript. We claim that the Lokad platform and Envision are superior for the _specific challenges_ faced by supply chain management. The platform eliminates entire classes of pitfalls that are simply unavoidable with general-purpose programming languages, while steering the development toward practices and technologies that are suited for the task at hand.

## A technical overview of Lokad

Let’s face it: the vast majority of the _Enterprise_ programming languages are barely good enough to qualify as “junk”. As we designed Envision, we decided to make it an awesome language only limited by its non-negotiable focus on supply chain optimization.

_This section is intended for professional software engineers who seek a high-level understanding of Envision, to see how it compares with alternative programming languages. If you just want to learn about Envision itself, you can skip this section._

**The language:**

* No arbitrary loops or branches (yes, it’s a feature)
* Strongly typed, no late binding
* Function calls are free of side-effects
* Algebras tailored for predictive optimization
* Differentiable Programming as a first-class citizen
* Calendar constructs as first-class citizen

Envision heavily leans toward the concise syntax of Python. We did borrow a few good ideas from other languages like SQL and CSS as well. However, unlike Python, Envision’s syntax is heavily geared toward _correctness by design_. Triggering a data pipeline crunching 1TB of relational data to get a runtime error 20 mins later leads to bad productivity and poor reliability once in production. Thus, Envision attempts to capture as many problems as possible at compile-time. In particular, we adopt the peculiar perspective that programs that are too slow to reliably run in production should not compile in the first place.

**The runtime:**

* Native code compilation targeting a _fleet_ of machines
* Concurrency by default through data parallelism
* Cooperative versioned big data file storage
* Fast re-executions through diff of the compute graphs
* Lightning fast execution with specialized algorithms (SIMD)
* Integrated layered memory management (RAM vs SSD vs remote storage)
* Data, scripts and runs are co-versioned

Speed is a feature, and when gigabytes of relational data are involved, hardware computing costs are nontrivial. Assuming that the code isn’t run through some kind of wacky interpreter, most of the compute inefficiencies lie in the _boundaries_ between subsystems within the data pipeline: between the filesystem and the program, between one library (e.g. NumPy) and another (e.g. TensorFlow), between the front-end and the backend, etc. Lokad largely eliminates all those layers through a unified distributed runtime. Under the hood, it’s memory mapped files, TCP sockets and SIMD algorithm, tightly integrated under a compiler-driven architecture.

**The development environment:**

Lokad offers a web IDE (Integrated Development Environment) intended for Supply Chain Scientists, complete with:

* Code coloring and code-autocompletion
* Smart compiler giving meaningful error messages
* Complete versioning of past edits and runs
* Contextual browsing of the input data
* Visual edition of dashboards (à la CSS editing)
* Propagate data comments cross-scripts

This environment is geared not only for high, individual productivity, but also for highly collaborative work with either fellow Supply Chain Scientists or supply chain practitioners - the ones who will consume the dashboards. The goal is to support fast paced prototyping, while giving a near immediate path toward production. Unlike visual tools, Lokad is actually suited for managing multiple pipelines, for example _testing_, _pre-production_ and _production_.

**Supporting tools**

* Fine-grained ACLs coupled with federated identity (SSO)
* Built-in orchestration with concurrency control and HTTP hooks
* Markdown edition and tabular previews for the file viewer
* FTPS / SFTP bridge to the internal file storage
* Built-in connectors for popular enterprise software (e.g. ERPs)
* Spreadsheet (i.e. Excel) web editing, importing, exporting

We adopt the _Batteries Included_ philosophy, removing the need for external tools or libraries to power the data pipeline, the numerical recipes and the reporting. Naturally, this approach comes with a razor-sharp focus on supply chain management. The supporting tools are tightly integrated with the rest of the environment.

## From a hacker perspective

The Lokad platform is a closed-source proprietary stack. Compared to most of our enterprise software competitors, merely having a detailed technical documentation _in the open_ is already notable. Some would argue that enterprise software vendors have a fairly low bar for openness. True. Lokad isn’t open source, not even close, not yet anyway. Nevertheless, there is a profound and counter-intuitive technical reason for this approach, which has nothing to do with intellectual property.

When we started designing Envision, we knew that mistakes would be made in the design of this language. Indeed, nearly all popular programming languages are cluttered with undesirable legacy features inherited from their early versions (cf. JavaScript and Python). Unfortunately, once a compiler - the program that turns source code into machine code - is in the open, it becomes immensely difficult to upgrade the language itself, because the slightest changes end up breaking an unknown amount of code in the wild.

By deciding to keep the entire Envision codebase within the Lokad platform, we gained the ability to automatically rewrite existing scripts whenever the Envision syntax was changing. This process is known as _transpilation_, i.e. source to source compilation. Since Envision’s  inception, we have completed over a hundred automated source code rewrites. In fact, as we knew that rewrites would unfortunately be part of our later daily development life, we engineered Envision itself to make those rewrites as straightforward as possible. Whenever a new language feature is introduced, this feature is always assessed with the question: how difficult will it be to de-entangle ourselves from this feature when the time comes?

In a few circumstances, when automated code writes weren’t even possible, as it happens when a subtle ambiguity is discovered and replaced by multiple non-ambiguous variants, the Lokad teams did manually perform the upgrade, _within days_, of every occurrence of the problem within our entire Envision codebase, reverse engineering scripts whenever needed. Doing this would have been impossible with an open source approach.

Furthermore, while open source software is awesome - as a matter of fact, Lokad is itself almost entirely built on top of open source materials - its track record when it comes to transparent upgrades is _dysmal_, and we are not exaggerating. The Python 2.x to 3.x transition took a decade. The JavaScript community has been rewriting its entire codebases every 18 months for a decade as well. Then, libraries and frameworks are even worse in this regard, as they frequently require extensive rewrites at every version, even seemingly minor ones.

Nevertheless, we have plans to make Envision more open _in time_. We will probably start with the development environment itself, then proceed with a local non-distributed version of Envision that remains to be developed, as we have no immediate needs or demands for it. Also, we are committed to remain open about what goes on _under the hood_.

This process will take years. We do not want to paint ourselves in a corner. Supply chains aren’t lifestyle apps. Then again, fail fast and break things is not an option. Software engineers frequently wonder why enterprise software is so bad. While some vendors are just negligent, the usual root cause is the sheer difficulty of upgrading the steam engine while it’s running at full speed and production depends on it.
