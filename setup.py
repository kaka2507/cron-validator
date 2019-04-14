from distutils.core import setup

setup(
    name='cron-validator',
    packages=['cron_validator'],
    version='1.0.0',
    license='MIT',
    description='Unix cron implementation by Python',
    author='vcoder',
    author_email='doanngocbao@gmail.com',
    url='https://github.com/vcoder4c/cron-validator',
    keywords=['cron', 'python', 'cron expression validator', 'cron expression iterator'],
    download_url='https://github.com/vcoder4c/cron-validator/archive/v1.0.0.tar.gz',
    install_requires=[
        'python_dateutil',
        'pytz'
    ]
)
