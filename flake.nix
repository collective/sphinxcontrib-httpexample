{
  description = "sphinxcontrib-httpexample";

  nixConfig = {
    extra-trusted-public-keys = "datakurre.cachix.org-1:ayZJTy5BDd8K4PW9uc9LHV+WCsdi/fu1ETIYZMooK78=";
    extra-substituters = "https://datakurre.cachix.org";
  };

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/release-24.05";
    nixpkgs-python27.url = "github:NixOS/nixpkgs/release-21.11";
    nixpkgs-pip2nix.url = "github:NixOS/nixpkgs/release-20.09";
    flake-compat = {
      url = "github:edolstra/flake-compat";
      flake = false;
    };
    gitignore = {
      url = "github:hercules-ci/gitignore.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    pip2nix.url = "github:nix-community/pip2nix";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.flake-utils.follows = "flake-utils";
    };
  };

  outputs =
    { self, ... }@inputs:
    inputs.flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs-python27 = import inputs.nixpkgs-python27 {
          inherit system;
          overlays = [
            (final: prev: {
              gitignoreSource = inputs.gitignore.lib.gitignoreSource;
              pip2nix =
                (import (inputs.pip2nix + "/release.nix") {
                  pkgs = import inputs.nixpkgs-pip2nix { inherit system; };
                }).pip2nix;
            })
          ];
          config = {
            permittedInsecurePackages = [
              "python2.7-Pillow-6.2.2"
              "python2.7-urllib3-1.26.2"
            ];
          };
        };
        pkgs = import inputs.nixpkgs {
          inherit system;
          overlays = [
            (final: prev: { gitignoreSource = inputs.gitignore.lib.gitignoreSource; })
            inputs.poetry2nix.overlays.default
          ];
        };
        build =
          python_: feature: install:
          (pkgs.poetry2nix.mkPoetryEnv rec {
            python = builtins.getAttr python_ pkgs;
            projectDir = ./.;
            pyproject = ./nix/poetry-${python_}-${feature}.toml;
            poetrylock = ./nix/poetry-${python_}-${feature}.lock;
            overrides = pkgs.poetry2nix.overrides.withDefaults (self: super: { });
            preferWheels = true;
            extraPackages =
              ps:
              if install == true then
                [
                  ps.pip
                  (pkgs.poetry2nix.mkPoetryApplication {
                    inherit
                      python
                      projectDir
                      pyproject
                      poetrylock
                      overrides
                      preferWheels
                      ;
                  })
                ]
              else
                [ ps.pip];
          });
      in
      {
        devShells = {
          pip2nix = (import ./setup.nix { pkgs = pkgs-python27; }).pip2nix;
          python27-docutils016 =
            (import ./setup.nix {
              pkgs = pkgs-python27;
              feature = "docutils016";
            }).develop;
          python27-docutils017 =
            (import ./setup.nix {
              pkgs = pkgs-python27;
              feature = "docutils017";
            }).develop;

          poetry = pkgs.mkShell { buildInputs = [ pkgs.poetry ]; };
          python39-docutils016 = (build "python39" "docutils016" true).env;
          python39-docutils017 = (build "python39" "docutils017" true).env;
          python39-docutils018 = (build "python39" "docutils018" true).env;
          python39-docutils019 = (build "python39" "docutils019" true).env;
          python39-docutils020 = (build "python39" "docutils020" true).env;
          python310-docutils016 = (build "python310" "docutils016" true).env;
          python310-docutils017 = (build "python310" "docutils017" true).env;
          python310-docutils018 = (build "python310" "docutils018" true).env;
          python310-docutils019 = (build "python310" "docutils019" true).env;
          python310-docutils020 = (build "python310" "docutils020" true).env;
          python311-docutils016 = (build "python311" "docutils016" true).env;
          python311-docutils017 = (build "python311" "docutils017" true).env;
          python311-docutils018 = (build "python311" "docutils018" true).env;
          python311-docutils019 = (build "python311" "docutils019" true).env;
          python311-docutils020 = (build "python311" "docutils020" true).env;
          python311-plone-sphinx-theme= (build "python311" "plone-sphinx-theme" true).env;
        };

        formatter = pkgs.nixfmt-rfc-style;
      }
    );
}
