{ buildPythonPackage
, fetchPypi
, h11
, multio
}:

buildPythonPackage rec {

  pname = "asks";
  version = "2.2.1";

  src = fetchPypi {
    inherit pname version;
    sha256 = "038rdaav027mn62r7ys5c1n9krli8f2j7nyzc6kpzinh0amfqynn";
  };

  doCheck = false;

  propagatedBuildInputs = [ 
    h11
    multio
  ];
}
