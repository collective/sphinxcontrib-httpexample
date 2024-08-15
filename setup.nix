# Legacy build for Python 2.7
{
  pkgs,
  python ? "python27",
  feature ? "docutils016",
  pythonPackages ? builtins.getAttr (python + "Packages") pkgs,
  requirements ? ./. + "/nix/requirements-${python}-${feature}.nix",
  src ? pkgs.gitignoreSource ./.,
  buildInputs ? with pkgs; [
    firefox
    geckodriver
    pandoc
  ],
  propagatedBuildInputs ? [ ],
  postShellHook ? "",
}:

with builtins;
with pkgs;
with pkgs.lib;

let

  # Aliases map from generated requirements to available nixpkgs packages
  aliases = {
    "Babel" = "babel";
    "backports.functools-lru-cache" = "backports_functools_lru_cache";
    "Jinja2" = "jinja2";
    "MarkupSafe" = "markupsafe";
    "pyOpenSSL" = "pyopenssl";
    "sphinx-rtd-theme" = "sphinx_rtd_theme";
  };

  # Packages that must override their respective nixpkgs versions
  override = [
    "coveralls"
    "docutils"
    "flake8"
    "pyOpenSSL"
    "pycodestyle"
    "pyflakes"
    "reportlab"
    "snapshottest"
    "sphinx"
    "sphinx_rtd_theme"
  ];

  # Target Python package overrides
  packageOverrides =
    lib.foldr lib.composeExtensions
      (self: super: {
        "backports_functools_lru_cache" = super."backports_functools_lru_cache".overridePythonAttrs (old: {
          postInstall = ''
            rm $out/${self.python.sitePackages}/backports/__init__.py
            rm $out/${self.python.sitePackages}/backports/__init__.pyc
          '';
        });
        "fastdiff" = super."fastdiff".overridePythonAttrs (old: {
          pipInstallFlags = [ "--no-dependencies" ];
          propagatedBuildInputs = [ ];
          doCheck = false;
        });
        "flake8-isort" = super."flake8-isort".overridePythonAttrs (old: {
          propagatedBuildInputs = old.propagatedBuildInputs ++ [ self."toml" ]; # Missing dep in nixpkgs-21.11
        });
        "sphinx" = super."sphinx".overridePythonAttrs (old: {
          patches = [ ]; # Patches for other version
        });
        "rst2pdf" = super."rst2pdf".overridePythonAttrs (old: {
          propagatedBuildInputs = old.propagatedBuildInputs ++ [ self."pillow" ]; # Missing dep in nixpkgs-21.11
        });
      })
      [
        # Import generated requirements not available in nixpkgs (or override them)
        (
          self: super:
          let
            generated = requirementsFunc self super;
          in

          # Import generated requirements not available
          (listToAttrs (
            map
              (name: {
                name = name;
                value = getAttr name generated;
              })
              (
                filter (
                  x: (!((hasAttr x pythonPackages) && (tryEval (getAttr x pythonPackages)).success))
                ) requirementsNames
              )

          ))
          //
            # Override nixpkgs version with version from generated requirements
            (listToAttrs (
              map
                (name: {
                  name = name;
                  value = (
                    (getAttr name super).overridePythonAttrs (
                      old:
                      let
                        pkg = (getAttr name generated);
                      in
                      {
                        inherit (pkg) pname version src;
                      }
                      //
                        # Change format when package could be overriden with wheel distribution
                        optionalAttrs (hasSuffix "whl" "${pkg.src}") {
                          format = "wheel";
                          patchPhase = "";
                          postPatch = "";
                        }
                    )
                  );
                })
                (
                  filter (
                    x: (hasAttr x pythonPackages) && (tryEval (getAttr x pythonPackages)).success && (elem x override)
                  ) requirementsNames
                )
            ))
        )

        # Map aliases required to align generated requirements with nixpkgs
        (
          self: super:
          (listToAttrs (
            map (name: {
              name = name;
              value = getAttr (getAttr name aliases) self;
            }) (attrNames aliases)
          ))
        )

        # Disable tests for speed and changes in versions
        (
          self: super:
          lib.mapAttrs (
            name: value:
            (
              if lib.isDerivation value && lib.hasAttr "overridePythonAttrs" value then
                value.overridePythonAttrs (_: {
                  doCheck = false;
                })
              else
                value
            )
          ) super
        )

        # Whatever else is necessary to make your stuff work
        (self: super: {
          # Fix hook after generic doCheck = false
          # "flitBuildHook" = super."flitBuildHook".override { flit = self."flit"; };
        })

      ];

  # Parsed setup.cfg in Nix via JSON (strings with \n are parsed into lists)
  setup_cfg = fromJSON (
    readFile (
      pkgs.runCommand "setup.json" { input = src + "/setup.cfg"; } ''
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
    )
  );

  # Helper to always return a list
  asList =
    name: attrs:
    if hasAttr name attrs then
      let
        candidate = getAttr name attrs;
      in
      if isList candidate then candidate else [ ]
    else
      [ ];

  # Import all generated requirements
  requirementsFunc = import requirements {
    inherit pkgs;
    inherit (builtins) fetchurl;
    inherit (pkgs) fetchgit fetchhg;
  };

  # List package names in generated requirements requirements
  requirementsNames = attrNames (requirementsFunc { } { });

  # TargetPython with all requirements
  targetPython = (pythonPackages.python.override { inherit packageOverrides; });

in
rec {

  # Shell with 'pip2nix' for resolving requirements.txt into requirements.nix
  pip2nix = mkShell {
    buildInputs = [
      nix
      nix-prefetch-git
      cacert
      (getAttr python pkgs.pip2nix)
    ];
  };

  # TargetPython with all requirements
  inherit targetPython;

  # final env with packages in requirements.txt
  env = pkgs.buildEnv {
    name = "env";
    paths = [ (targetPython.withPackages (ps: map (name: getAttr name ps) requirementsNames)) ];
  };

  # Final package
  package = targetPython.pkgs.buildPythonPackage {
    pname = setup_cfg.metadata.name;
    version = setup_cfg.metadata.version;
    src = cleanSource src;
    doCheck = false;
    nativeBuildInputs =
      [
        pkgs.gnumake
        pkgs.nix
      ]
      ++ buildInputs
      ++ map (name: getAttr name targetPython.pkgs) (asList "setup_requires" setup_cfg.options);
    checkInputs =
      buildInputs
      ++ map (name: getAttr name targetPython.pkgs) (asList "tests_require" setup_cfg.options);
    propagatedBuildInputs =
      propagatedBuildInputs
      ++ map (name: getAttr name targetPython.pkgs) (asList "install_requires" setup_cfg.options);
    postShellHook =
      ''
        export PYTHONPATH=$(pwd)/src:$PYTHONPATH
      ''
      + postShellHook;
  };

  install = targetPython.withPackages (ps: [ package ]);

  develop = package.overridePythonAttrs (old: {
    name = "${old.pname}-shell";
    nativeBuildInputs =
      with pkgs;
      [
        cacert
        gnumake
        git
        entr
        nix
        env
      ]
      ++ buildInputs
      ++ propagatedBuildInputs;
    postShellHook = ''
      export PYTHONPATH=$(pwd)/src:$PYTHONPATH
      export PATH=${env}/bin:$PATH
    '';
  });

  shell = develop;

}
