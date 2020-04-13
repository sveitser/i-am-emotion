{ buildPythonPackage
, fetchPypi
, trio
}:

buildPythonPackage rec {

  pname = "multio";
  version = "0.2.5";

  src = fetchPypi {
    inherit pname version;
    sha256 = "17zph1qns5l4nqbcyhbbnx72v47hghpnr98w9gsajg85ipa9pkgx";
  };

  doCheck = false;

  propagatedBuildInputs = [
    trio
  ];
}
