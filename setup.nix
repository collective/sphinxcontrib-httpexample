{ pkgs ? import ./nix {}
, sources ? import ./nix/sources.nix {}
, python ? "python39"
, feature ? ""
, pythonPackages ? builtins.getAttr (python + "Packages") pkgs
, requirements ?  ./. + "/nix/requirements-${python}${feature}.nix"
, src ? pkgs.gitignoreSource ./.
, buildInputs ? with pkgs; []
, propagatedBuildInputs ? []
}:

with builtins;
with pkgs;
with pkgs.lib;

let

  # Parse setup.cfg into Nix via JSON (strings with \n are parsed into lists)
  setup_cfg = fromJSON(readFile(
    pkgs.runCommand "setup.json" { input=src + "/setup.cfg"; } ''
      ${pkgs.python3}/bin/python << EOF
      import configparser, json, re, os
      parser = configparser.ConfigParser()
      with open(os.environ.get("input"), errors="ignore",
                encoding="ascii") as fp:  # fromJSON supports ASCII only
         parser.read_file(fp)
      with open(os.environ.get("out"), "w") as fp:
        fp.write(json.dumps(dict(
          [(k, dict([(K, "\n" in V and [re.findall(r"[\w\.-]+", i)[0] for i in
                                        filter(bool, V.split("\n"))] or V)
                     for K, V in v.items()]))
           for k, v in parser._sections.items()]
        ), indent=4, sort_keys=True))
      fp.close()
      EOF
    ''
  ));

  # Requirements for generating requirements.nix
  requirementsBuildInputs = [ cacert nix nix-prefetch-git
                              libffi postgresql ];

  # Load generated requirements
  requirementsFunc = import requirements {
    inherit pkgs;
    inherit (builtins) fetchurl;
    inherit (pkgs) fetchgit fetchhg;
  };

  # List package names in requirements
  requirementsNames = attrNames (requirementsFunc {} {});

  # Return base name from python drv name or name when not python drv
  pythonNameOrName = drv:
    if hasAttr "pythonModule" drv then drv.pname else drv.name;

  # Merge named input list from nixpkgs drv with input list from requirements drv
  mergedInputs = old: new: inputsName: self: super:
    (attrByPath [ inputsName ] [] new) ++ map
    (x: attrByPath [ (pythonNameOrName x) ] x self)
    (filter (x: !isNull x) (attrByPath [ inputsName ] [] old));

  # Merge package drv from nixpkgs drv with requirements drv
  mergedPackage = old: new: self: super:
    if isString new.src
       && !isNull (match ".*\.whl" new.src)  # do not merge build inputs for wheels
       && new.pname != "wheel"               # ...
    then new.overridePythonAttrs(old: rec {
      propagatedBuildInputs =
        mergedInputs old new "propagatedBuildInputs" self super;
    })
    else old.overridePythonAttrs(old: rec {
      inherit (new) pname version src;
      name = "${pname}-${version}";
      checkInputs =
        mergedInputs old new "checkInputs" self super;
      buildInputs =
        mergedInputs old new "buildInputs" self super;
      nativeBuildInputs =
        mergedInputs old new "nativeBuildInputs" self super;
      propagatedBuildInputs =
        mergedInputs old new "propagatedBuildInputs" self super;
      doCheck = false;
    });

  # Build python with manual aliases for naming differences between world and nix
  buildPython = (pythonPackages.python.override {
    packageOverrides = self: super:
      listToAttrs (map (name: {
        name = name; value = getAttr (getAttr name aliases) super;
      }) (filter (x: hasAttr (getAttr x aliases) super) (attrNames aliases)));
  });

  # Build target python with all generated & customized requirements
  targetPython = (buildPython.override {
    packageOverrides = self: super:
      # 1) Merge packages already in pythonPackages
      let super_ = (requirementsFunc self buildPython.pkgs);  # from requirements
          results = (listToAttrs (map (name: let new = getAttr name super_; in {
        inherit name;
        value = mergedPackage (getAttr name buildPython.pkgs) new self super_;
      })
#     (filter (name: trace name hasAttr "overridePythonAttrs"
      (filter (name: hasAttr "overridePythonAttrs"
                     (if (tryEval (attrByPath [ name ] {} buildPython.pkgs)).success
                      then (attrByPath [ name ] {} buildPython.pkgs) else {}))
       requirementsNames)))
      // # 2) with packages only in requirements or disabled in nixpkgs
      (listToAttrs (map (name: { inherit name; value = (getAttr name super_); })
      (filter (name: (! ((hasAttr name buildPython.pkgs) &&
                         (tryEval (getAttr name buildPython.pkgs)).success)))
       requirementsNames)));
      in # 3) finally, apply overrides (with aliased drvs mapped back)
      (let final = (super // (results //
        (listToAttrs (map (name: {
          name = getAttr name aliases; value = getAttr name results;
        }) (filter (x: hasAttr x results) (attrNames aliases))))
      )); in (final // (overrides self final)));
    self = buildPython;
  });

  # Helper to always return a list
  asList = name: attrs:
    if hasAttr name attrs then
      let candidate = getAttr name attrs; in
      if isList candidate then candidate else []
    else [];

  # Alias packages with different names in requirements and in nixpkgs
  aliases = {
    "Pillow" = "pillow";
    "pillow" = "Pillow";
  };

  # Final overrides to fix issues all the magic above cannot fix automatically
  overrides = self: super: if buildPython.pkgs.isPy27 then {
    "backports.functools-lru-cache" = super."backports.functools-lru-cache".overridePythonAttrs(old: {
      postInstall = ''
        rm $out/${self.python.sitePackages}/backports/__init__.py
        rm $out/${self.python.sitePackages}/backports/__init__.pyc
      '';
    });
    "coveralls" = super."coveralls".overridePythonAttrs(old: {
      propagatedBuildInputs = old.propagatedBuildInputs ++ [ self."pyOpenSSL" ];
    });
    "fastdiff" = super."fastdiff".overridePythonAttrs(old: {
      pipInstallFlags = ["--no-dependencies"];
      propagatedBuildInputs = [];
      doCheck = false;
    });
    "configparser" = buildPython.pkgs."configparser";
    "contextlib2" = buildPython.pkgs."contextlib2";
    "importlib-metadata" = buildPython.pkgs."importlib-metadata";
    "more-itertools" = buildPython.pkgs."more-itertools";
    "packaging" = buildPython.pkgs."packaging";
    "pathlib2" = buildPython.pkgs."pathlib2";
    "pyparsing" = buildPython.pkgs."pyparsing";
    "scandir" = buildPython.pkgs."scandir";
    "six" = buildPython.pkgs."six";
    "zipp" = buildPython.pkgs."zipp";
  } else {
    "packaging" = buildPython.pkgs."packaging";
    "pyparsing" = buildPython.pkgs."pyparsing";
    "six" = buildPython.pkgs."six";
  };

in rec {

  inherit buildPython targetPython;

  # final env with packages in requirements.txt
  env = pkgs.buildEnv {
    name = "env";
    paths = [
      (targetPython.withPackages(ps: map (name: getAttr name ps) requirementsNames))
    ];
  };

  # final shell with packages in requirements.txt
  shell = package.overridePythonAttrs(old: {
    name = "${old.pname}-shell";
    nativeBuildInputs = with pkgs; [ cacert gnumake git entr nix env vault ]
      ++ buildInputs ++ propagatedBuildInputs;
  });

  # final package
  package = targetPython.pkgs.buildPythonPackage {
    pname = setup_cfg.metadata.name;
    version = setup_cfg.metadata.version;
    src = cleanSource src;
    doCheck = true;
    nativeBuildInputs = [ pkgs.gnumake pkgs.nix ] ++ buildInputs ++ map
      (name: getAttr name targetPython.pkgs) (asList "setup_requires" setup_cfg.options);
    checkInputs = buildInputs ++ map
      (name: getAttr name targetPython.pkgs) (asList "tests_require" setup_cfg.options);
    propagatedBuildInputs = propagatedBuildInputs ++ map
      (name: getAttr name targetPython.pkgs) (asList "install_requires" setup_cfg.options);
    postShellHook = ''
      export PYTHONPATH=$(pwd)/src:$PYTHONPATH
      export PATH=${env}/bin:$PATH
    '';
  };

}
