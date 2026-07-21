{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    ros2nix_repo = {
      url = "github:wentasah/ros2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    {
      self,
      nixpkgs,
      ros2nix_repo,
    }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs {
        inherit system;
        overlays = [
          (final: prev: {
            ros2nix = ros2nix_repo.packages.${system}.default;
          })
        ];
      };
    in
    {
      devShells.${system}.default = pkgs.mkShellNoCC {
        name = "ros-NUR-helper";
        inputsFrom = with self.packages.${system}; [
          ros-NUR-helper
        ];
      };
      packages.${system} = {
        ros-NUR-helper = pkgs.callPackage ./package.nix { };
        default = self.packages.${system}.ros-NUR-helper;
      };
    };
}
