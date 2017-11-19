{ pkgs ? import <nixpkgs> {}
, python ? "python3"
, support ? (import ./nix-support { inherit pkgs python; })
}:

with pkgs.lib;
with support;

pythonPackages.buildPythonPackage {
  name = "${setup.metadata.name}-${setup.metadata.version}";
  src = cleanSource ./.;
  buildInputs = map
    (name: getAttr name pythonPackages) (setup.options.setup_requires ++
                                         setup.options.tests_require);
  propagatedBuildInputs = map
    (name: getAttr name pythonPackages) setup.options.install_requires;
  doCheck = false;
}
