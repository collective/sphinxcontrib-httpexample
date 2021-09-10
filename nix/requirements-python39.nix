# Generated by pip2nix 0.8.0.dev1
# See https://github.com/nix-community/pip2nix

{ pkgs, fetchurl, fetchgit, fetchhg }:

self: super: {
  "Jinja2" = super.buildPythonPackage rec {
    pname = "Jinja2";
    version = "2.11.3";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/7e/c2/1eece8c95ddbc9b1aeb64f5783a9e07a286de42191b7204d67b7496ddf35/Jinja2-2.11.3-py2.py3-none-any.whl";
      sha256 = "06clnbqhhklyk9x21dy5l1ms4rm9m3ffshsay2ixc79kcg87mr03";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [
      self."MarkupSafe"
    ];
  };
  "MarkupSafe" = super.buildPythonPackage rec {
    pname = "MarkupSafe";
    version = "1.1.1";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/b9/2e/64db92e53b86efccfaea71321f597fa2e1b2bd3853d8ce658568f7a13094/MarkupSafe-1.1.1.tar.gz";
      sha256 = "0sqipg4fk7xbixqd8kq6rlkxj664d157bdwbh93farcphf92x1r9";
    };
    format = "setuptools";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "alabaster" = super.buildPythonPackage rec {
    pname = "alabaster";
    version = "0.7.12";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/10/ad/00b090d23a222943eb0eda509720a404f531a439e803f6538f35136cae9e/alabaster-0.7.12-py2.py3-none-any.whl";
      sha256 = "0nfkvlqp1mwjj0jjqk0mm7hk5c6rq5l1dpm2bva5pq50rjykhr24";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "astunparse" = super.buildPythonPackage rec {
    pname = "astunparse";
    version = "1.6.3";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/2b/03/13dde6512ad7b4557eb792fbcf0c653af6076b81e5941d36ec61f7ce6028/astunparse-1.6.3-py2.py3-none-any.whl";
      sha256 = "1s5qlkxwcjv752hx2ksw0wj69y7kplly6nl8bhrbpdf8y8bj8rf2";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [
      self."six"
      self."wheel"
    ];
  };
  "attrs" = super.buildPythonPackage rec {
    pname = "attrs";
    version = "21.2.0";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/20/a9/ba6f1cd1a1517ff022b35acd6a7e4246371dfab08b8e42b829b6d07913cc/attrs-21.2.0-py2.py3-none-any.whl";
      sha256 = "1cdh2v3scv9mi00195khsch3y6l8wvq0rmjsjmxdn85cv3b917hl";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "babel" = super.buildPythonPackage rec {
    pname = "babel";
    version = "2.9.1";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/aa/96/4ba93c5f40459dc850d25f9ba93f869a623e77aaecc7a9344e19c01942cf/Babel-2.9.1-py2.py3-none-any.whl";
      sha256 = "1yfyn32hlv60sr0knymcb4msvd3slmcv4z5ny08wsdyrj4my2jdb";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [
      self."pytz"
    ];
  };
  "certifi" = super.buildPythonPackage rec {
    pname = "certifi";
    version = "2020.12.5";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/5e/a0/5f06e1e1d463903cf0c0eebeb751791119ed7a4b3737fdc9a77f1cdfb51f/certifi-2020.12.5-py2.py3-none-any.whl";
      sha256 = "0c4qsp7q10hhiryvl6dyxsfh9r1mpja8sfkzri2bvf9kkvxp96ki";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "chardet" = super.buildPythonPackage rec {
    pname = "chardet";
    version = "4.0.0";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/19/c7/fa589626997dd07bd87d9269342ccb74b1720384a4d739a1872bd84fbe68/chardet-4.0.0-py2.py3-none-any.whl";
      sha256 = "198xs99vbvcj312d1bk7bgn7aix5h64sqi3hwvr1i4gxcr6har7q";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "coverage" = super.buildPythonPackage rec {
    pname = "coverage";
    version = "5.5";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/38/df/d5e67851e83948def768d7fb1a0fd373665b20f56ff63ed220c6cd16cb11/coverage-5.5.tar.gz";
      sha256 = "0b112ly7vvplvm9l411aqknxhr7fzfyp28xhflhkcx78l3lqzrzb";
    };
    format = "setuptools";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "coveralls" = super.buildPythonPackage rec {
    pname = "coveralls";
    version = "3.0.1";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/54/f5/a6431412a456267b43b03ebd3670d8e196754f5280a2409a4c9ceaccf192/coveralls-3.0.1-py2.py3-none-any.whl";
      sha256 = "118knhqjnqnjhrpnhh4p1src4z0jh3qqhg06lcdnccsp8arp7lbv";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [
      self."coverage"
      self."docopt"
      self."requests"
    ];
  };
  "docopt" = super.buildPythonPackage rec {
    pname = "docopt";
    version = "0.6.2";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/a2/55/8f8cab2afd404cf578136ef2cc5dfb50baa1761b68c9da1fb1e4eed343c9/docopt-0.6.2.tar.gz";
      sha256 = "14f4hn6d1j4b99svwbaji8n2zj58qicyz19mm0x6pmhb50jsics9";
    };
    format = "setuptools";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "docutils" = super.buildPythonPackage rec {
    pname = "docutils";
    version = "0.16";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/81/44/8a15e45ffa96e6cf82956dd8d7af9e666357e16b0d93b253903475ee947f/docutils-0.16-py2.py3-none-any.whl";
      sha256 = "1bxk9azs910d03ldns9kw8wj6xlybk6iam9z8caj8xppzfnphnqc";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "flake8" = super.buildPythonPackage rec {
    pname = "flake8";
    version = "3.9.2";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/fc/80/35a0716e5d5101e643404dabd20f07f5528a21f3ef4032d31a49c913237b/flake8-3.9.2-py2.py3-none-any.whl";
      sha256 = "01q927ija7hhqnqbxsdlwvd4wf53ydg90iwddrhlz13d6hrx73xz";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [
      self."mccabe"
      self."pycodestyle"
      self."pyflakes"
    ];
  };
  "flake8-blind-except" = super.buildPythonPackage rec {
    pname = "flake8-blind-except";
    version = "0.2.0";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/4e/23/097032baef8d317748580c32cd5fd9346d71c7b4b015b1d3f6b36f3f603e/flake8-blind-except-0.2.0.tar.gz";
      sha256 = "1r84ya26czdwk2vv8abryp9i83av0dw0gzm30v005dlwl6hn1a02";
    };
    format = "setuptools";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [
      self."setuptools"
    ];
  };
  "flake8-coding" = super.buildPythonPackage rec {
    pname = "flake8-coding";
    version = "1.3.2";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/83/a8/0de26928c40727ec29289b4f5c751a75e4cdd639faed9ab01b835fd0883c/flake8_coding-1.3.2-py2.py3-none-any.whl";
      sha256 = "0q12c7cpgrxw0c1vcv8la8yhgxy341mffrc9djmx82adqh942w3r";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [
      self."flake8"
    ];
  };
  "flake8-debugger" = super.buildPythonPackage rec {
    pname = "flake8-debugger";
    version = "4.0.0";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/6b/57/f722ba8b09c8e8b1b851a71ebec1f9cef5577c7b9271ae2b4d8fd405e005/flake8_debugger-4.0.0-py3-none-any.whl";
      sha256 = "0chh15yf430isjwn4z02pjkzzv5qxc17ah0003fip3g1fam4zrl2";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [
      self."poetry-core"
    ];
    propagatedBuildInputs = [
      self."flake8"
      self."pycodestyle"
      self."six"
    ];
  };
  "flake8-isort" = super.buildPythonPackage rec {
    pname = "flake8-isort";
    version = "4.0.0";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/39/ef/2bda8933e8c36c0a02c6bb29ae9dac303dceea7316e81b3d01bf6a9145b6/flake8_isort-4.0.0-py2.py3-none-any.whl";
      sha256 = "0g1grrnf8pvysqg95psz47hpi76p0my6hdz3vq99ard3kgpxd73j";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [
      self."flake8"
      self."isort"
      self."testfixtures"
    ];
  };
  "flake8-polyfill" = super.buildPythonPackage rec {
    pname = "flake8-polyfill";
    version = "1.0.2";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/86/b5/a43fed6fd0193585d17d6faa7b85317d4461f694aaed546098c69f856579/flake8_polyfill-1.0.2-py2.py3-none-any.whl";
      sha256 = "1sdrd40l01p130dx6c3jmpvda9jqnpkhadd7kjqrbdrsxqs6mghj";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [
      self."flake8"
    ];
  };
  "flake8-quotes" = super.buildPythonPackage rec {
    pname = "flake8-quotes";
    version = "3.2.0";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/80/d0/e257f4435cf930bc85182b0c44e6ceb539e095dc982ab26ef7d1e28c6455/flake8-quotes-3.2.0.tar.gz";
      sha256 = "0ph5s6lxgpzz4an0ax6s5xjqypqmngwr5b1i0h9pqhzghplic49z";
    };
    format = "setuptools";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [
      self."flake8"
    ];
  };
  "idna" = super.buildPythonPackage rec {
    pname = "idna";
    version = "2.10";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/a2/38/928ddce2273eaa564f6f50de919327bf3a00f091b5baba8dfa9460f3a8a8/idna-2.10-py2.py3-none-any.whl";
      sha256 = "1h280sli58v5dapmf79rnnqdrrk0xjn8vi3pxppknllv3r5q0zdr";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "imagesize" = super.buildPythonPackage rec {
    pname = "imagesize";
    version = "1.2.0";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/31/b2/b5522a0c8d11e4aff83f8342f3f0dea68c2fb25aa44403e420587f0ce204/imagesize-1.2.0-py2.py3-none-any.whl";
      sha256 = "1898hacrsc6y5jfz3rkaqdagi7q6fcjblzfaigacff90dadg2rb9";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "importlib-metadata" = super.buildPythonPackage rec {
    pname = "importlib-metadata";
    version = "4.0.1";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/8e/e2/49966924c93909d47612bb47d911448140a2f6c1390aec2f4c1afbe3748f/importlib_metadata-4.0.1-py3-none-any.whl";
      sha256 = "0pa68jj8wfnmzb2rnc2j5f3mbymwwg4lqy11pvw8cq3adpm1vsyp";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [
      self."zipp"
    ];
  };
  "iniconfig" = super.buildPythonPackage rec {
    pname = "iniconfig";
    version = "1.1.1";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/9b/dd/b3c12c6d707058fa947864b67f0c4e0c39ef8610988d7baea9578f3c48f3/iniconfig-1.1.1-py2.py3-none-any.whl";
      sha256 = "1cx8kpp3akxwadzsmv2cdnifkyzj8fki5frmv3mzcivz9g3287h1";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "isort" = super.buildPythonPackage rec {
    pname = "isort";
    version = "5.8.0";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/d9/47/0ec3ec948b7b3a0ba44e62adede4dca8b5985ba6aaee59998bed0916bd17/isort-5.8.0-py3-none-any.whl";
      sha256 = "0pb5dniglf91zs3nqa9qw829z64sl15ivknv8jckq7i1ml56ic9b";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "mccabe" = super.buildPythonPackage rec {
    pname = "mccabe";
    version = "0.6.1";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/87/89/479dc97e18549e21354893e4ee4ef36db1d237534982482c3681ee6e7b57/mccabe-0.6.1-py2.py3-none-any.whl";
      sha256 = "0hhdp0srgrv4bmzlzvmk67zrqr9cvkjjzgd4gmkvd90dhrc652mb";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "packaging" = super.buildPythonPackage rec {
    pname = "packaging";
    version = "20.9";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/3e/89/7ea760b4daa42653ece2380531c90f64788d979110a2ab51049d92f408af/packaging-20.9-py2.py3-none-any.whl";
      sha256 = "0yll40y48lgh45z5axlzyvlixgama5cmrh2r9032w1dwyyklswb7";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [
      self."pyparsing"
    ];
  };
  "pep8-naming" = super.buildPythonPackage rec {
    pname = "pep8-naming";
    version = "0.11.1";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/44/57/d6544d56909f5fc77e24dd6c6727c33cd8d06c67828ecb05c650f3ec95ec/pep8_naming-0.11.1-py2.py3-none-any.whl";
      sha256 = "0f37045x6p17hiy97xpgr9n4gwj7mc3n8zfhnpl763byx8zgwfzl";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [
      self."flake8-polyfill"
    ];
  };
  "pillow" = super.buildPythonPackage rec {
    pname = "pillow";
    version = "8.2.0";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/21/23/af6bac2a601be6670064a817273d4190b79df6f74d8012926a39bc7aa77f/Pillow-8.2.0.tar.gz";
      sha256 = "1qf3bz1sfz58ff6hclg8phgqyy210x3aqdk5yzjr8m5vsw8ap1x7";
    };
    format = "setuptools";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "pluggy" = super.buildPythonPackage rec {
    pname = "pluggy";
    version = "0.13.1";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/a0/28/85c7aa31b80d150b772fbe4a229487bc6644da9ccb7e427dd8cc60cb8a62/pluggy-0.13.1-py2.py3-none-any.whl";
      sha256 = "0b8x12j6394w3spk8xzp991khyv8102gas1q7hn515iwv1f18v4n";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "poetry-core" = super.buildPythonPackage rec {
    pname = "poetry-core";
    version = "1.0.3";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/bf/e1/08c7478df1e93dea47b06c9d9a80dbb54af7421462e1b22c280d063df807/poetry_core-1.0.3-py2.py3-none-any.whl";
      sha256 = "16lf41zc0axs18i80bqpfln3scp7cs6spq8k80wfhb8ia5if9gf6";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "py" = super.buildPythonPackage rec {
    pname = "py";
    version = "1.10.0";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/67/32/6fe01cfc3d1a27c92fdbcdfc3f67856da8cbadf0dd9f2e18055202b2dc62/py-1.10.0-py2.py3-none-any.whl";
      sha256 = "12l1326xbn82inp4b1a6lvnnr3xb4djdlip012hymznilrm8701v";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "pycodestyle" = super.buildPythonPackage rec {
    pname = "pycodestyle";
    version = "2.7.0";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/de/cc/227251b1471f129bc35e966bb0fceb005969023926d744139642d847b7ae/pycodestyle-2.7.0-py2.py3-none-any.whl";
      sha256 = "0s1062z8jw6111c7505vggh982cp6w52yiw0crfbbh7w33cpcksi";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "pyflakes" = super.buildPythonPackage rec {
    pname = "pyflakes";
    version = "2.3.1";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/6c/11/2a745612f1d3cbbd9c69ba14b1b43a35a2f5c3c81cd0124508c52c64307f/pyflakes-2.3.1-py2.py3-none-any.whl";
      sha256 = "1hzgabzbyaxj0n4zlp6rxvjriw2gv3adzmvjvl8ria5q04ypi4vq";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "pygments" = super.buildPythonPackage rec {
    pname = "pygments";
    version = "2.9.0";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/a6/c9/be11fce9810793676017f79ffab3c6cb18575844a6c7b8d4ed92f95de604/Pygments-2.9.0-py3-none-any.whl";
      sha256 = "13iv73575lilrm01ffhr8y8sxn8kxhvfqsgwckbr919725280vnn";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "pyparsing" = super.buildPythonPackage rec {
    pname = "pyparsing";
    version = "2.4.7";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/8a/bb/488841f56197b13700afd5658fc279a2025a39e22449b7cf29864669b15d/pyparsing-2.4.7-py2.py3-none-any.whl";
      sha256 = "12y8xwjb118a4jqvvfg9k90kqg03n4d3ygb5csz0l81wxy4pb7gg";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "pytest" = super.buildPythonPackage rec {
    pname = "pytest";
    version = "6.2.4";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/a1/59/6821e900592fbe261f19d67e4def0cb27e52ef8ed16d9922c144961cc1ee/pytest-6.2.4-py3-none-any.whl";
      sha256 = "1438jzl65f4l73h3l50ympb22wiiqp2yl20zdzvyhsxxm4qj3vwi";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [
      self."attrs"
      self."iniconfig"
      self."packaging"
      self."pluggy"
      self."py"
      self."toml"
    ];
  };
  "pytest-cov" = super.buildPythonPackage rec {
    pname = "pytest-cov";
    version = "2.12.0";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/2c/70/184e8f4804b21dca4d78b6b76414c9d3b29cedbdef7ba28cdf14fe7de3e0/pytest_cov-2.12.0-py2.py3-none-any.whl";
      sha256 = "0vh6cp0m4i5bx5wjmaw1771r03d3v80rick0pdvs7kxsrcyr7m4m";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [
      self."coverage"
      self."pytest"
    ];
  };
  "pytest-runner" = super.buildPythonPackage rec {
    pname = "pytest-runner";
    version = "5.3.0";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/40/96/9024a1c07bbe5e16bdcbcbd021b608e37b32df4301ae2090aad27c24ffe6/pytest_runner-5.3.0-py3-none-any.whl";
      sha256 = "0xvf9lflrhhnghc4296kwwkj0vcy1wf5rw4w6qmxwlm7mpcmk2a4";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "pytz" = super.buildPythonPackage rec {
    pname = "pytz";
    version = "2021.1";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/70/94/784178ca5dd892a98f113cdd923372024dc04b8d40abe77ca76b5fb90ca6/pytz-2021.1-py2.py3-none-any.whl";
      sha256 = "1607gl2x9290ks5sa6dvqw9dgg1kwdf9fj9xcb9jw19nfwzcw47b";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "pyyaml" = super.buildPythonPackage rec {
    pname = "pyyaml";
    version = "5.4.1";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/a0/a4/d63f2d7597e1a4b55aa3b4d6c5b029991d3b824b5bd331af8d4ab1ed687d/PyYAML-5.4.1.tar.gz";
      sha256 = "0pm440pmpvgv5rbbnm8hk4qga5a292kvlm1bh3x2nwr8pb5p8xv0";
    };
    format = "setuptools";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "reportlab" = super.buildPythonPackage rec {
    pname = "reportlab";
    version = "3.5.67";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/2a/02/078c875d81f231fc11ecda3158a2e2cfccc390a534c316e2524db007e245/reportlab-3.5.67.tar.gz";
      sha256 = "1jc6zr1a0kprxawjaaybdwgd1wnpkaxi57nkicn7bjpvfdn21whc";
    };
    format = "setuptools";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [
      self."pillow"
    ];
  };
  "requests" = super.buildPythonPackage rec {
    pname = "requests";
    version = "2.25.1";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/29/c1/24814557f1d22c56d50280771a17307e6bf87b70727d975fd6b2ce6b014a/requests-2.25.1-py2.py3-none-any.whl";
      sha256 = "07l7fm7y9zkvmpfli803dni6iwyyhy1f804y46wycam46r70h462";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [
      self."certifi"
      self."chardet"
      self."idna"
      self."urllib3"
    ];
  };
  "rst2pdf" = super.buildPythonPackage rec {
    pname = "rst2pdf";
    version = "0.98";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/ec/b1/5e1d8d769fd2e713eda3bb75d7a46a8ef660119909f180d282df64b79ce2/rst2pdf-0.98-py3-none-any.whl";
      sha256 = "0s829p7mwq474wn18hqnx7bhm6m5g1qx4rnck4whdvxfwicnsfr6";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [
      self."Jinja2"
      self."docutils"
      self."importlib-metadata"
      self."packaging"
      self."pygments"
      self."reportlab"
      self."smartypants"
    ];
  };
  "six" = super.buildPythonPackage rec {
    pname = "six";
    version = "1.16.0";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/d9/5a/e7c31adbe875f2abbb91bd84cf2dc52d792b5a01506781dbcf25c91daf11/six-1.16.0-py2.py3-none-any.whl";
      sha256 = "0m02dsi8lvrjf4bi20ab6lm7rr6krz7pg6lzk3xjs2l9hqfjzfwa";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "smartypants" = super.buildPythonPackage rec {
    pname = "smartypants";
    version = "2.0.1";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/da/ed/1da76d11aa858ee23dac5b52d9ac2db7df02b89f7679d5d8970bcd44b59c/smartypants-2.0.1-py2.py3-none-any.whl";
      sha256 = "03cgh2jlrmm03424xlh3fzrlqsqikv6kfq58b2qib3ghpmy7zfcd";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "snapshottest" = super.buildPythonPackage rec {
    pname = "snapshottest";
    version = "0.5.0";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/38/9d/6114ac51327ee8be784ebde5fb21606e161097a41eac3e0619bfc7fad0fd/snapshottest-0.5.0.tar.gz";
      sha256 = "035ljn22x11qgkllvr6h72zik5nkh9xqnz8fbai73lbz77mjhp11";
    };
    format = "setuptools";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [
      self."six"
      self."termcolor"
    ];
  };
  "snowballstemmer" = super.buildPythonPackage rec {
    pname = "snowballstemmer";
    version = "2.1.0";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/f6/6e/7e07970c90a57c21da92013c5ba47f8e9598c17e88cc35b008ca61225ed3/snowballstemmer-2.1.0-py2.py3-none-any.whl";
      sha256 = "1hpdblr2cs2rxilaiz338k5x9awai1m14l5n2f69dyc5x9xl86xm";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "sphinx" = super.buildPythonPackage rec {
    pname = "sphinx";
    version = "4.0.1";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/a7/5b/50ccdef4683ffac13fdf4cc80fa9ced84849fd4eca444dec22e6c937a1e2/Sphinx-4.0.1-py3-none-any.whl";
      sha256 = "1l5rv2zk8p04zsrbvgi2qx3agx71dpalg30r6zpscdwp6dgnymmj";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [
      self."Jinja2"
      self."MarkupSafe"
      self."alabaster"
      self."babel"
      self."docutils"
      self."imagesize"
      self."packaging"
      self."pygments"
      self."requests"
      self."setuptools"
      self."snowballstemmer"
      self."sphinxcontrib-applehelp"
      self."sphinxcontrib-devhelp"
      self."sphinxcontrib-htmlhelp"
      self."sphinxcontrib-jsmath"
      self."sphinxcontrib-qthelp"
      self."sphinxcontrib-serializinghtml"
    ];
  };
  "sphinx-rtd-theme" = super.buildPythonPackage rec {
    pname = "sphinx-rtd-theme";
    version = "0.5.2";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/ac/24/2475e8f83519b54b2148d4a56eb1111f9cec630d088c3ffc214492c12107/sphinx_rtd_theme-0.5.2-py2.py3-none-any.whl";
      sha256 = "0vvxk0496sc9prv5w0rp6bs78z3pqvmj62p205xdfihlifzbs1aa";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [
      self."docutils"
      self."sphinx"
    ];
  };
  "sphinx-testing" = super.buildPythonPackage rec {
    pname = "sphinx-testing";
    version = "1.0.1";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/52/b8/f5636c938e52b35d08afcec23d1c1162f177941cc584b4687026a98c4f9a/sphinx_testing-1.0.1-py2.py3-none-any.whl";
      sha256 = "1jbbb2c5i0grhbwi2m8k703h4bgl7vp7ip901s074l8cmvmb2b4z";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [
      self."six"
      self."sphinx"
    ];
  };
  "sphinxcontrib-applehelp" = super.buildPythonPackage rec {
    pname = "sphinxcontrib-applehelp";
    version = "1.0.2";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/dc/47/86022665a9433d89a66f5911b558ddff69861766807ba685de2e324bd6ed/sphinxcontrib_applehelp-1.0.2-py2.py3-none-any.whl";
      sha256 = "0nl8mw0kxd0544ws9c9gcplikzbv4zzfghf4kv19ggk2x7ji2qc0";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "sphinxcontrib-devhelp" = super.buildPythonPackage rec {
    pname = "sphinxcontrib-devhelp";
    version = "1.0.2";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/c5/09/5de5ed43a521387f18bdf5f5af31d099605c992fd25372b2b9b825ce48ee/sphinxcontrib_devhelp-1.0.2-py2.py3-none-any.whl";
      sha256 = "0bjafgjc3lbw9h6bq8q49hjjbwvi50fx67pygypw2p1kk8zj4rc1";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "sphinxcontrib-htmlhelp" = super.buildPythonPackage rec {
    pname = "sphinxcontrib-htmlhelp";
    version = "1.0.3";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/36/62/8222554b29b3acde8420128d6d3999c5904d40922ef4b6ccb370e2be7421/sphinxcontrib_htmlhelp-1.0.3-py2.py3-none-any.whl";
      sha256 = "0vx8rkvw46j6s9jisnq9bi4anyf8mxnysp686yn41qs15i5c42rw";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "sphinxcontrib-httpdomain" = super.buildPythonPackage rec {
    pname = "sphinxcontrib-httpdomain";
    version = "1.7.0";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/79/35/6f43bde0c4ead866c349a1fa0ff732a31613b3f462ad9b9630c03a958f41/sphinxcontrib_httpdomain-1.7.0-py2.py3-none-any.whl";
      sha256 = "07hr70zjw70yavz9xabvsfi7mgl221s9xiyirn0g22yp0x83gd8z";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [
      self."six"
      self."sphinx"
    ];
  };
  "sphinxcontrib-jsmath" = super.buildPythonPackage rec {
    pname = "sphinxcontrib-jsmath";
    version = "1.0.1";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/c2/42/4c8646762ee83602e3fb3fbe774c2fac12f317deb0b5dbeeedd2d3ba4b77/sphinxcontrib_jsmath-1.0.1-py2.py3-none-any.whl";
      sha256 = "0y1i21qwi5p5f98jxds8r1n12yj12la6nrkkiq3z5wvqzgmymhif";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "sphinxcontrib-qthelp" = super.buildPythonPackage rec {
    pname = "sphinxcontrib-qthelp";
    version = "1.0.3";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/2b/14/05f9206cf4e9cfca1afb5fd224c7cd434dcc3a433d6d9e4e0264d29c6cdb/sphinxcontrib_qthelp-1.0.3-py2.py3-none-any.whl";
      sha256 = "1dps9m29ay339v0shix314qac2imh7kavjjfzm8qv2klrd5w57xx";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "sphinxcontrib-serializinghtml" = super.buildPythonPackage rec {
    pname = "sphinxcontrib-serializinghtml";
    version = "1.1.4";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/9a/ca/bfad79b79b3821d0c6361c431f0ef4aec16ee248338b2c2013008b34d345/sphinxcontrib_serializinghtml-1.1.4-py2.py3-none-any.whl";
      sha256 = "16jsvf8jj20qg9imp7kglvlqxqkl9mfnzwawirx62n9z88fshhpj";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "termcolor" = super.buildPythonPackage rec {
    pname = "termcolor";
    version = "1.1.0";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/8a/48/a76be51647d0eb9f10e2a4511bf3ffb8cc1e6b14e9e4fab46173aa79f981/termcolor-1.1.0.tar.gz";
      sha256 = "0fv1vq14rpqwgazxg4981904lfyp84mnammw7y046491cv76jv8x";
    };
    format = "setuptools";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "testfixtures" = super.buildPythonPackage rec {
    pname = "testfixtures";
    version = "6.17.1";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/9c/93/08cbd1203cd490ac789f42a9594540d1b6c4d8fca6c2d06296b284518052/testfixtures-6.17.1-py2.py3-none-any.whl";
      sha256 = "0dwir7f9n31s6flvbxw08n7n1q0n3qj3n1fz2zxf46cnyn1ixlwy";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "toml" = super.buildPythonPackage rec {
    pname = "toml";
    version = "0.10.2";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/44/6f/7120676b6d73228c96e17f1f794d8ab046fc910d781c8d151120c3f1569e/toml-0.10.2-py2.py3-none-any.whl";
      sha256 = "16sgpg57kxx5jh467d9qwc2hwshfvdbl0xkafdp3qspvbfp46qc0";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "urllib3" = super.buildPythonPackage rec {
    pname = "urllib3";
    version = "1.26.5";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/0c/cd/1e2ec680ec7b09846dc6e605f5a7709dfb9d7128e51a026e7154e18a234e/urllib3-1.26.5-py2.py3-none-any.whl";
      sha256 = "0z2siwabara1prpr8vbqhmcx11m6jh1y9kr6v2cqyr96vxs06fkm";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "zipp" = super.buildPythonPackage rec {
    pname = "zipp";
    version = "3.4.1";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/0f/8c/715c54e9e34c0c4820f616a913a7de3337d0cd79074dd1bed4dd840f16ae/zipp-3.4.1-py3-none-any.whl";
      sha256 = "161hw31ysqssxamjjjxvmp0aahpfhvr8f5rxb7fhj5k2ak66djsi";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
}