from setuptools import find_packages, setup

package_name = "emotion_nodes"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="spark",
    maintainer_email="spark@example.com",
    description="ROS2 nodes for emotion pipeline",
    license="Proprietary",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "emotion_frame_sampler = emotion_nodes.emotion_frame_sampler:main",
        ],
    },
)
