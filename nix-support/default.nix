{ pkgs ? import <nixpkgs> {}
, python ? "python3"
}:

with builtins;
with pkgs.lib;

let

  setup = fromJSON(readFile(
    pkgs.runCommand "setup.json" { input=../setup.cfg; } ''
      ${pkgs.python3}/bin/python << EOF
      import configparser, json, os
      parser = configparser.ConfigParser()
      parser.read(os.environ.get("input"))
      with open(os.environ.get("out"), "w") as fp:
        fp.write(json.dumps(dict(
          [(k, dict([(K, "\n" in V and list(filter(bool, V.split("\n"))) or V)
                     for K, V in v.items()]))
           for k, v in parser._sections.items()]
        ), indent=4, sort_keys=True))
      fp.close()
      EOF
    ''
  ));

  pythonPackages = builtins.getAttr (python + "Packages") pkgs;

  requirements = import ./requirements.nix {
    inherit pkgs;
    inherit (pkgs) fetchurl fetchgit fetchhg;
  };

  overrides = import ./overrides.nix {
    inherit pkgs pythonPackages;
  };

  packages =
    (fix
    (extends overrides
    (extends requirements
             pythonPackages.__unfix__)));

in

{

  setup = setup;

  pythonPackages = packages;

  env = packages.python.withPackages (ps: map
    (name: getAttr name packages) (attrNames (requirements {} {})));

  shell = (packages.python.withPackages (ps: map
    (name: getAttr name packages) (attrNames (requirements {} {})))).env;

  pip2nix = (pkgs.python3.withPackages (ps: [
    (import (pkgs.fetchFromGitHub {
      owner = "johbo";
      repo = "pip2nix";
      rev = "714b51eb69711474a9a2fbddf144e5e66b36986b";
      sha256 = "0h7hg95p1v392h4a310ng2kri9r59ailpj3r4mkr6x1dhq6l4fic";
    } + "/release.nix") {}).pip2nix.python36
  ])).env;

}
