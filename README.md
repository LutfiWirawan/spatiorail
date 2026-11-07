# SpatioRail

**From Spatial Data to Production, Reliably.**

SpatioRail is an application-agnostic, spatial-native workflow
orchestration framework for building, executing, validating, versioning,
and releasing geospatial data pipelines.

It is designed to connect GIS applications, spatial data sources,
processing engines, and external services through a consistent pipeline
and worker architecture. Rather than being tied to a single GIS
application or processing engine, SpatioRail aims to provide the
infrastructure for managing geospatial workflows across different
environments.

> **Project status:** Early-stage design and development. The
> capabilities described below represent the project direction and
> roadmap; they should not be interpreted as a claim that every feature
> is already implemented.

## Repository description

**Recommended GitHub description:**

> A spatial-native workflow orchestration framework for geospatial
> processing, distributed workers, data validation, versioning, and
> reliable production releases.

**Short tagline:**

> From Spatial Data to Production, Reliably.

## Why SpatioRail?

Geospatial workflows often span multiple tools, formats, databases,
processing engines, and applications. Managing these workflows reliably
requires more than running isolated GIS scripts.

SpatioRail aims to provide a common orchestration layer for:

-   Defining pipelines as dependency-aware Directed Acyclic Graphs
    (DAGs).
-   Scheduling and executing jobs through worker processes.
-   Connecting different spatial processing engines and data sources.
-   Processing large datasets with streaming, chunking, and
    bounded-memory strategies.
-   Validating spatial outputs before they are promoted.
-   Tracking executions, artifacts, lineage, and versions.
-   Releasing approved outputs and rolling back to earlier releases when
    necessary.

## Design principles

-   **Application-agnostic** --- integrate with WebGIS, QGIS, ArcGIS,
    geoportals, and custom applications through APIs, SDKs, and worker
    protocols.
-   **Spatial-native** --- treat geospatial data, operations,
    validation, and lifecycle management as first-class concepts.
-   **Engine-agnostic** --- avoid coupling orchestration to a single
    spatial processing engine.
-   **Worker-based** --- allow processing workers to run independently
    and, as the system evolves, across multiple machines.
-   **Scalable by design** --- favor streaming, chunking, partitioning,
    bounded memory, and backpressure over loading entire datasets into
    memory.
-   **Reproducible** --- retain execution metadata, artifact references,
    versions, and lineage.
-   **Safe by default** --- distinguish a successful execution from an
    approved production release.

## Conceptual architecture

``` text
GIS Applications / External Systems
              |
         REST API / SDK
              |
          Control Plane
              |
   Queue / Events / Worker Protocol
              |
         Worker Runtime
              |
     Spatial Engines & Adapters
              |
      Data and Artifact Layer
```

### Control plane

The control plane coordinates pipeline definitions and job lifecycles.
Its planned responsibilities include:

-   API Gateway
-   Pipeline Registry
-   Scheduler
-   Job Queue
-   Execution Manager
-   Version Manager
-   Approval and Policy
-   Monitoring and Audit

### Worker runtime

Workers perform the actual tasks. The architecture is intended to
support multiple worker types, including:

-   Native spatial workers
-   Python workers
-   External workers implemented in languages such as Go, Rust, Java, or
    Node.js
-   Container-based workers

External workers should communicate through a stable protocol rather
than depending on a C++ ABI.

### Spatial processing foundation

The initial technology direction favors proven spatial libraries:

-   **GDAL** for geospatial data access and format handling.
-   **GEOS** for geometry operations.
-   **PROJ** for coordinate reference system transformations.
-   **Apache Arrow** where columnar data interchange is beneficial.

Python is the proposed primary language for orchestration and the
control plane. Native C/C++ components may be used where existing
libraries or measured performance requirements justify them.

## Pipeline lifecycle

A pipeline may move through stages such as:

``` text
INGEST
  -> BUILD / TRANSFORM
  -> TEST / VALIDATE
  -> VERIFY
  -> REVIEW / APPROVAL
  -> DEPLOY
  -> MONITOR
  -> ROLLBACK (when required)
```

A key design distinction is that **execution, artifact, and release are
separate concepts**:

-   A **pipeline** defines the workflow.
-   An **execution** is an attempt to run that workflow.
-   An **artifact** is an output produced by processing.
-   A **release** is an artifact or set of outputs that has passed the
    required checks and has been promoted.

A successful execution should not automatically overwrite production
data. Promotion should be governed by validation and, where appropriate,
explicit approval.

## Large-data strategy

SpatioRail is intended for workloads that may involve large vector and
raster datasets. Its design direction emphasizes:

-   Streaming and chunk-based processing.
-   Bounded memory usage.
-   Spatial partitioning where appropriate.
-   Controlled parallelism and concurrency limits.
-   Backpressure between pipeline stages.
-   Passing artifact references and metadata between tasks instead of
    transferring entire datasets through queues or keeping them all in
    memory.
-   Immutable artifacts where practical.
-   Incremental processing and caching where they provide measurable
    benefits.

Performance optimization should be guided by benchmarks. The project
does not aim to reimplement established libraries such as GDAL, GEOS, or
PROJ without a demonstrated need.

## Technology direction

  -----------------------------------------------------------------------
  Area                                Initial direction
  ----------------------------------- -----------------------------------
  Control plane and orchestration     Python

  Spatial processing                  GDAL, GEOS, PROJ

  Native extensions                   C/C++ when justified

  Metadata and initial queue          PostgreSQL
  persistence                         

  API                                 REST / HTTP

  Worker communication                HTTP-based protocol initially; gRPC
                                      / Protocol Buffers may be evaluated

  Artifact storage                    Local filesystem initially;
                                      S3-compatible storage later

  Data interchange                    Apache Arrow where useful

  SDK                                 Python first; TypeScript later
  -----------------------------------------------------------------------

These are architectural directions, not immutable implementation
requirements. Technology choices may be refined as the project is
prototyped and benchmarked.

## Roadmap

The development plan is intentionally incremental.

1.  **Core foundation** --- project package, job model, execution
    lifecycle, PostgreSQL-backed queue, basic worker, REST API, status,
    logs, and retry.
2.  **Spatial runtime** --- GDAL, GEOS, and PROJ integration; initial
    vector/raster operators; streaming and chunking; validation.
3.  **Pipeline system** --- DAG execution, dependency resolution,
    timeout, cancellation, scheduling, and an initial Python SDK.
4.  **Data lifecycle** --- artifact registry, dataset snapshots, spatial
    diff, quality gates, approval, release, and rollback.
5.  **Ecosystem** --- external worker protocol, additional SDKs,
    plugin/operator registry, service adapters, dashboard, and
    distributed workers.

## Guiding decisions

-   Do not pass entire datasets through the job queue.
-   Do not require every worker to use the same programming language.
-   Do not couple external workers to a C++ ABI.
-   Do not equate execution success with production release.
-   Do not discard execution history when rolling back.
-   Do not build every planned component before validating the core
    architecture.
-   Benchmark before introducing custom native optimizations.

## Who is SpatioRail for?

SpatioRail is intended for teams and developers who need to automate and
govern geospatial data workflows across applications and infrastructure,
including:

-   GIS and WebGIS platform teams.
-   Spatial data engineering teams.
-   Geoportal and geospatial service operators.
-   Organizations managing recurring geospatial ETL and data-quality
    workflows.
-   Developers integrating spatial processing into larger applications.

## License

The recommended license for SpatioRail is **Apache License 2.0**.

Apache-2.0 is a permissive open-source license that includes an explicit
patent grant and provisions relevant to contributions. The final
repository should include the complete Apache License 2.0 text and a
`NOTICE` file if required by the project's distribution and attribution
needs.

> License selection is a project-owner decision. Confirm the license
> before publishing the repository or accepting external contributions.

------------------------------------------------------------------------

SpatioRail is being designed as infrastructure for dependable geospatial
data pipelines---not as a replacement for GIS desktop applications or
established spatial processing libraries.
