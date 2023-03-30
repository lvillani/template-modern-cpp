#include <iostream>

#include <spdlog/spdlog.h>

#include <project_version/project_version.h>

int main() {
    spdlog::info("Hello, world.");

    spdlog::info("Project version:");
    spdlog::info("String: {}", project_version());
    spdlog::info("Major: {}", project_version_major());
    spdlog::info("Minor: {}", project_version_minor());
    spdlog::info("Patch: {}", project_version_patch());
    spdlog::info("Tweak: {}", project_version_tweak());

    return 0;
}
