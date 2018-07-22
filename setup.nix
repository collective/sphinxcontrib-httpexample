{ pkgs ? import (builtins.fetchTarball {
    # update sha256 with value of "nix-prefetch-url --unpack [url]"
    url = "https://github.com/NixOS/nixpkgs-channels/archive/d6c6c7fcec6dbd2b8ab14f0b35d56c7733872baa.tar.gz";
    sha256 = "1bq59575b58lmh5w8bh7pwp17c3p2nm651bz1i3q224c4zsj9294";  # nixos-18.03 at 2018-07-22
  }) {}
, python ? "python3"
, pythonPackages ? builtins.getAttr (python + "Packages") pkgs
, setup ? import (builtins.fetchTarball {
    # update sha256 with value of "nix-prefetch-url --unpack [url]"
    url = "https://github.com/datakurre/setup.nix/archive/v1.0.tar.gz";
    sha256 = "1m8hpz2yxdj1j4zmpbxqakhi2gjjb8nlik4r8ijf1hlax76ncj4y";
  })
}:

with pkgs.lib;

let overrides = self: super: {
  "coveralls" = super."coveralls".overridePythonAttrs(old: {
    buildInputs = [ self."pytest-runner" ];
    propagatedBuildInputs = old.propagatedBuildInputs
      ++ optionals self.isPy27 [ self."ipaddress" self."pyopenssl" ];
  });
  "flake8-isort" = super."flake8-isort".overridePythonAttrs(old: {
    buildInputs = optionals self.isPy27 [ self."futures" ];
  });
  "isort" = super."isort".overridePythonAttrs(old: {
    buildInputs = optionals self.isPy27 [ self."futures" ];
  });
  "pytest" = super."pytest".overridePythonAttrs(old: {
    buildInputs = old.buildInputs
      ++ optionals self.isPy27 [ self."funcsigs" ];
    propagatedBuildInputs = old.propagatedBuildInputs
      ++ optionals self.isPy27 [ self."funcsigs" ];
  });
  "pytest-cov" = super."pytest-cov".overridePythonAttrs(old: {
    buildInputs = optionals self.isPy27 [ self."funcsigs" ];
  });
};

in setup {
  inherit pkgs pythonPackages overrides;
  src = ./.;
}
