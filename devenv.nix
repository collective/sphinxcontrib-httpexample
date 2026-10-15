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
        "pycrypto"
        "secretstorage"
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
      # libcst (required by the editable hook) comes from nixpkgs (1.8.6) via
      # pyproject-build-systems and pins a PyO3 too old for Python 3.15;
      # remove once nixpkgs has libcst >= 1.9
      "libcst" = prev."libcst".overrideAttrs (
        old:
        pkgs.lib.optionalAttrs (final.python.pythonAtLeast "3.15") {
          env = (old.env or { }) // {
            PYO3_USE_ABI3_FORWARD_COMPATIBILITY = "1";
          };
        }
      );
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
    pkgs.treefmt
    pkgs.nixfmt
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
}
