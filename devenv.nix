{ pkgs, ... }:
{
  imports = [
    ./devenv.uv2nix.nix
  ];

  languages.python.pyprojectOverrides =
    final: prev:
    let
      packagesToBuildWithSetuptools = [
        "cmarkgfm"
        "docopt"
        "markupsafe"
      ];
    in
    {
      "hatchling" = prev."hatchling".overrideAttrs (old: {
        propagatedBuildInputs = [ final."editables" ];
      });
      "cffi" = prev."cffi".overrideAttrs (old: {
        buildInputs = [ pkgs.libffi ];
        nativeBuildInputs =
          old.nativeBuildInputs
          ++ final.resolveBuildSystem ({
            "setuptools" = [ ];
          });
      });
    }
    // builtins.listToAttrs (
      map (pkg: {
        name = pkg;
        value = prev.${pkg}.overrideAttrs (old: {
          nativeBuildInputs =
            old.nativeBuildInputs
            ++ final.resolveBuildSystem ({
              "setuptools" = [ ];
            });
        });
      }) packagesToBuildWithSetuptools
    );

  packages = [
    pkgs.gnumake
    pkgs.gnused
  ];

  dotenv.disableHint = true;

  enterShell = ''
    unset PYTHONPATH
    export UV_NO_SYNC=1
    export UV_PYTHON_DOWNLOADS=never
    export REPO_ROOT=$(git rev-parse --show-toplevel)
  '';

  enterTest = ''
    make test
  '';

  cachix.pull = [ "datakurre" ];

  git-hooks.hooks.treefmt = {
    enable = true;
    settings.formatters = [
      pkgs.nixfmt-rfc-style
    ];
  };
}
