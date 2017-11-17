#!/usr/bin/env nix-shell
{ pkgs ? (import ./nix-support {}).pkgs
, python ? "python3"
, pythonPackages ? (import ./nix-support { inherit python; }).pythonPackages
}:

with builtins;
with pkgs.lib;

let

  name = head (
    match ".*name = ([^\n]+).*" (
      readFile ./setup.cfg));

  version = head (
    match ".*version = ([^\n]+).*" (
      readFile ./setup.cfg));

  parse = from: to: splitString "\n" (
    replaceStrings [" "] [""] (
      head (
        match ".*${from} =\n(.*)\n${to}.*" (
          readFile ./setup.cfg))));

  setup_requires   = parse "setup_requires"   "install_requires";
  install_requires = parse "install_requires" "tests_require";
  tests_require    = parse "tests_require"   "package_dir";

in

pythonPackages.buildPythonPackage {
  name = "${name}-${version}";
  src = cleanSource ./.;
  buildInputs = map
    (name: getAttr name pythonPackages) (setup_requires ++ tests_require);
  propagatedBuildInputs = map
    (name: getAttr name pythonPackages) install_requires;
  doCheck = false;
}
