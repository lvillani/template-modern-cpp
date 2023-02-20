# Modern C++ Template Project

A template project using C++ 20, CMake, and modern practices.

## Choices

This repository follows, for the most part, advice taken from the book [Professional CMake: A
Practical Guide](https://crascit.com/professional-cmake/).

The following list illustrates some additional choices and their rationale:

- Ninja as the default build tool: Ninja is available on most platforms, is designed to be fast and,
  when available, is preferred by [Qt Creator](https://doc.qt.io/qtcreator/) and recommended by [VS
  Code CMake Tools](https://github.com/microsoft/vscode-cmake-tools/blob/main/docs/configure.md). It
  is rapidly becoming the most recommended build tool.
- Single configuration builds: [almost all
  generators](https://cmake.org/cmake/help/latest/prop_gbl/GENERATOR_IS_MULTI_CONFIG.html) are
  single-config and IDEs like [Qt Creator](https://doc.qt.io/qtcreator/) work better with them.
