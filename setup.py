from setuptools import setup, find_packages

setup(
    name="mailbridge",
    version="0.1.0",
    description="Flexible mail sending library for multiple providers: SMTP, SendGrid, Mailgun,  Amazon SES, Postmark, Brevo (Sendinblue)",
    author="Radomir Brkovic",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    python_requires=">=3.10",
    extras_require={
        "smtp": [],
        "ses": ["boto3>=1.26.0"],
        "sendgrid": ["requests>=2.28.0"],
        "mailgun": ["requests>=2.28.0"],
        "postmark": ["requests>=2.28.0"],
        "brevo": ["requests>=2.28.0"],
        "all": ["boto3>=1.26.0", "requests>=2.28.0"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)