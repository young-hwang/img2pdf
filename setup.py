from setuptools import find_packages, setup


setup(
    name="scan2pdf",
    version="0.1.0",
    description="Normalize scanned images and export a single PDF.",
    packages=find_packages(include=["scan2pdf", "scan2pdf.*"]),
    install_requires=["Pillow>=10.0"],
    extras_require={"deskew": ["opencv-python>=4.8"]},
    entry_points={"console_scripts": ["scan2pdf=scan2pdf.cli:main"]},
)
