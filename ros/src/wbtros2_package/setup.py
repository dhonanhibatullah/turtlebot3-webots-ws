import os
from glob import glob
from setuptools import setup

package_name = 'wbtros2_package'
package_list = [
    package_name,
    package_name + '/modules'
]

setup(
    name                = package_name,
    version             = '0.0.0',
    packages            = package_list,
    data_files          = [
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*_launch.py'))
    ],
    install_requires    = ['setuptools'],
    zip_safe            = True,
    maintainer          = 'dhonan',
    maintainer_email    = 'dhonan.hibatullah@gmail.com',
    description         = 'None',
    license             = 'None',
    tests_require       = ['pytest'],
    entry_points        = {
        'console_scripts': [
            'wbtros2_ros2handler = wbtros2_package.wbtros2_ros2handler:main'
        ],
    },
)
