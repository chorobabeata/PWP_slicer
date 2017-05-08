cmake_minimum_required(VERSION 2.8.9)

project(PWP_lab)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/PWP_lab")
set(EXTENSION_CATEGORY "Examples")
set(EXTENSION_CONTRIBUTORS "Beata Choroba (IB)")
set(EXTENSION_DESCRIPTION "PWP lab 6")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/PWP_lab.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/PWP_lab/Screenshots/1.png")

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(ScrModule)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_CPACK})
