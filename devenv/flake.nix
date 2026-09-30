{
  description = "A reproducible container built with Nix";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };

  outputs = { nixpkgs, flake-parts, ... } @ inputs:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [ "x86_64-linux" ];
      perSystem = {pkgs, system, ... }: {
        packages.container = pkgs.dockerTools.buildLayeredImage {
          name = "protocol-challenge-devenv";
          tag = "latest";
          contents = with pkgs; [
            coreutils
            bash
            verilator
            mill
            python3
            rustc
            cargo
            (callPackage ./customasm.nix { })
          ];

          config = {
            Cmd = [ "bash" ];
            Volumes = {
              "/home" = {};
              "/data" = {};
            };
            WorkingDir = "/home";
          };
        };
      };
    };
}

