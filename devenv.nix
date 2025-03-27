{ pkgs, ... }:
{
  imports = [
    ./devenv/modules/python.nix
  ];

  languages.python.pyprojectOverrides = final: prev: {
    "hatchling" = prev."hatchling".overrideAttrs (old: {
      propagatedBuildInputs = [ final."editables" ];
    });
    "docopt" = prev."docopt".overrideAttrs (old: {
      nativeBuildInputs =
        old.nativeBuildInputs
        ++ final.resolveBuildSystem ({
          "setuptools" = [ ];
        });

    });
  };

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
