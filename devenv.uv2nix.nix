{
  pkgs,
  config,
  lib,
  inputs,
  ...
}:
let
  cfg = config.languages.python;
  inherit (lib) types mkOption;
  python = cfg.interpreter;
  workspace = inputs.uv2nix.lib.workspace.loadWorkspace {
    workspaceRoot = config.languages.python.workspaceRoot;
  };
  overlay = workspace.mkPyprojectOverlay {
    sourcePreference = "wheel";
    dependencies = {
      "${cfg.pyprojectName}" = cfg.dependencies;
    };
  };
  pythonSet =
    (pkgs.callPackage inputs.pyproject-nix.build.packages {
      inherit python;
    }).overrideScope
      (
        pkgs.lib.composeManyExtensions [
          inputs.pyproject-build-systems.overlays.default
          overlay
          cfg.pyprojectOverrides
        ]
      );
  editableOverlay = workspace.mkEditablePyprojectOverlay {
    root = "$REPO_ROOT";
  };
  editablePythonSet = pythonSet.overrideScope editableOverlay;
in
{
  options.languages.python = {
    interpreter = mkOption {
      default = pkgs.python3;
      type = types.package;
    };
    dependencies = mkOption {
      default = [
        "rf711"
        "dev"
      ];
      type = types.listOf types.str;
    };
    workspaceRoot = mkOption {
      type = types.path;
      default = ./.;
    };
    pyprojectName = mkOption {
      type = types.str;
      default =
        (builtins.fromTOML (builtins.readFile (cfg.workspaceRoot + "/pyproject.toml"))).project.name;
    };
    pyprojectOverrides = mkOption {
      default = final: prev: {
      };
    };
  };
  config = {
    languages.python = {
      uv.package = pkgs.buildFHSEnv {
        name = "uv";
        targetPkgs = pkgs: [
          inputs.uv2nix.packages.x86_64-linux.uv-bin
          python
        ];
        runScript = "uv";
      };
    };
    packages = [
      cfg.uv.package
      config.outputs.python.virtualenv
    ];
    outputs.python =
      let
        pyprojectName =
          (builtins.fromTOML (builtins.readFile (cfg.workspaceRoot + "/pyproject.toml"))).project.name;
      in
      {
        virtualenv = editablePythonSet.mkVirtualEnv "${pyprojectName}-dev-env" {
          "${cfg.pyprojectName}" = cfg.dependencies;
        };
      };
  };
}
