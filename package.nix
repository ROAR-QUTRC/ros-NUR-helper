{
  lib,
  ros2nix,
  python3Packages,
}:
let
  inherit (python3Packages) buildPythonApplication setuptools gitpython;
in
buildPythonApplication {
  pname = "ros-NUR-helper";
  version = "0.0.0";
  src = lib.cleanSource ./.;
  pyproject = true;
  build-system = [ setuptools ];
  propagatedBuildInputs = [
    ros2nix
    gitpython
  ];
  allowSubstitutes = false;
  meta = {
    mainProgram = "ros-NUR-helper.py";
  };
}
