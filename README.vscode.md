# common ML error in M1/Tensorflow for resolve VSCode enviroment


Here is my .vsocde/setting for working enviroment of this
```json
{
    "python.linting.pylintArgs": [
        "--ignored-modules=tensorflow.keras"
    ],
    "python.analysis.diagnosticSeverityOverrides": {
        "reportUnusedImport": "information",
        "reportMissingImports": "none"
    }
}

```