#include <iostream>

#include <project_version/project_version.h>

int main() {
    std::cout << "Hello, world." << std::endl;

    std::cout << "Project version:" << std::endl;
    std::cout << "String: " << project_version() << std::endl;
    std::cout << "Major: " << project_version_major() << std::endl;
    std::cout << "Minor: " << project_version_minor() << std::endl;
    std::cout << "Patch: " << project_version_patch() << std::endl;
    std::cout << "Tweak: " << project_version_tweak() << std::endl;

    return 0;
}
