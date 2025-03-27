{
  pkgs,
  config,
  lib,
  inputs,
  ...
}:
let
  cfg = config.package.editor;
  extensions = inputs.nix-vscode-extensions.extensions.${pkgs.system};
  inherit (lib) types mkOption;
in
{
  packages = [
    (pkgs.vscode-with-extensions.override {
      vscodeExtensions = [
        pkgs.vscode-extensions.bbenoist.nix
        pkgs.vscode-extensions.ms-pyright.pyright
        pkgs.vscode-extensions.ms-python.python
        pkgs.vscode-extensions.ms-python.debugpy
        pkgs.vscode-extensions.ms-vscode.makefile-tools
        pkgs.vscode-extensions.vscodevim.vim
        (pkgs.vscode-extensions.charliermarsh.ruff.overrideAttrs (old: {
          postInstall = ''
            rm -f $out/share/vscode/extensions/charliermarsh.ruff/bundled/libs/bin/ruff
            ln -s ${pkgs.ruff}/bin/ruff $out/share/vscode/extensions/charliermarsh.ruff/bundled/libs/bin/ruff
          '';
        }))
        extensions.vscode-marketplace.tamasfe.even-better-toml
        pkgs.vscode-extensions.github.copilot
        pkgs.vscode-extensions.github.copilot-chat
      ];
    })
  ];
}
