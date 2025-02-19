# Docs

## Introduction

This is where the Napytau documentation is maintained. It is built with the `mkdocs` framework, using the `material` theme. The directory structure should be as follows:

```
.
└── root(docs/docs)
    ├── ressources
    │   └── <any ressources (images, etc.) you want to include
    ├── index.md (Landing Page)
    └── <module name>
        ├── ressources (should be maintained per module, if necessary)
        │   └── <any ressources (images, etc.) you want to include
        └── <module related sub page name> (Module Related Sub Page)
```

## Local Development

To build the docs locally run this command in the `/docs` directory:

```bash
$ mkdocs serve
```

## Webpage update

The webpage hosted on GitHub is automatically updated to reflect the current state of the docs, after every new commit to the `main` branch. This is done via the `/.github/workflows/build_docs.yml` workflow.