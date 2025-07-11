import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="robotframework-dbus",
	version="0.1",
	author="damies13",
	author_email="damies13+robotframeworkdbus@gmail.com",
	description="robotframework-dbus",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/damies13/robotframework-dbus",
	packages=setuptools.find_packages(exclude=["build/*"]),
	install_requires=['dbus-python', 'requests', 'robotframework>=5'],
	classifiers=[
		"Development Status :: 4 - Beta",
		"Framework :: Robot Framework",
		"Framework :: Robot Framework :: Library",
		"Topic :: Software Development :: Testing",
		"Topic :: Software Development :: Testing :: Acceptance",
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Operating System :: POSIX :: Linux",
		"Environment :: X11 Applications",
		"Environment :: X11 Applications :: Gnome",
		"Environment :: X11 Applications :: KDE",
		"Environment :: Wayland Applications",
		"Environment :: Wayland Applications :: Gnome",
		"Environment :: Wayland Applications :: KDE",
		"Topic :: Desktop Environment :: Gnome",
		"Topic :: Desktop Environment :: K Desktop Environment (KDE)",
	],
	python_requires='>=3.8',
	project_urls={
		'Getting Help': 'https://github.com/damies13/robotframework-dbus',
		'Source': 'https://github.com/damies13/robotframework-dbus',
	},
)
