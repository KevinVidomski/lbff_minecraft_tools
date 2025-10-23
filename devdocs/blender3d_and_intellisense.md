# Gemini AI Overview

To achieve Blender add-on development with Intellisense in VS Code, including the bpy module, follow these steps:

1. Install VS Code and Python Extension:
1. Download and install Visual Studio Code from its official website.
1. Open VS Code, go to the Extensions view (Ctrl+Shift+X), search for "Python," and install the official Microsoft Python extension.
1. Install the Blender Development Extension:
1. In VS Code, open the Extensions view again.
1. Search for "Blender Development" (authored by Jacques Lucke) and install it. This extension facilitates integration between VS Code and Blender.
1. Configure Blender Executable Path:
1. Open the VS Code Command Palette (Ctrl+Shift+P).
1. Search for "Blender: Start" and select it.
1. You will be prompted to choose the path to your Blender executable. Select the correct Blender executable for the version you are developing for.
1. Generate Fake bpy Module for Intellisense:

## Fake bpy Module for Intellisense

While the Blender Development extension helps with general integration, for robust Intellisense for the bpy module, you can use the fake-bpy-module project.

This project generates a "fake" bpy module that provides type hints and stubs for Blender's API, enabling VS Code's Intellisense to offer accurate autocompletion and suggestions.

Follow the instructions on the fake-bpy-module GitHub repository to install and generate the module. Typically, this involves using pip to install the package and then running a command to generate the stubs for your specific Blender version.

## Link fake-bpy-module in VS Code

Once the fake-bpy-module is generated, you need to tell your VS Code project to use it for Intellisense.

In your VS Code workspace settings (.vscode/settings.json), add or modify the python.analysis.extraPaths setting to include the directory where the generated fake_bpy_module is located.

```python

    {
        "python.analysis.extraPaths": [
            "path/to/your/fake_bpy_module" // Replace with the actual path
        ]
    }
```

## Start Developing

Create or open your Blender add-on's Python files (.py) in VS Code.

With the fake-bpy-module correctly configured, you should now have comprehensive Intellisense for bpy and other Blender API elements, including autocompletion, signature help, and type checking.

Use the "Blender: Run Script" command from the VS Code Command Palette to execute your scripts within a running Blender instance for testing.
