# ROS NUR Helper

A tool to autogenerate nix derivations from ROS package.xml files, using
configuration from a toml file. Wrapper around
[ros2nix](https://github.com/wentasah/ros2nix), adding functionality for static
config files over passing urls to command line.

Designed to be used to update derivations for third-party packages not contained
in [nix-ros-overlay](https://github.com/lopsided98/nix-ros-overlay).

Examples of config files can be found in the examples/ directory.

## Usage

With flakes enabled:

```{bash}
nix run github:ROAR-QUTRC/ros-NUR-helper -- -c path/to/config/file.toml
```

If anyone wants to use this without flakes, PRs are welcome.
