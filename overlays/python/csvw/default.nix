{ buildPythonPackage
, fetchPypi
, dateutil
, rfc3986
, pytest
, isodate
, uritemplate
}:

buildPythonPackage rec {

  pname = "csvw";
  version = "1.4.5";

  src = fetchPypi {
    inherit pname version;
    sha256 = "0xydjmxa39xbfnf5y9v1kkwyslg9jb8g6bvlsqhr3m22cbyn9p9i";
  };

  prePatch = ''
    echo DUMMY > LICENSE
  '';

  checkInputs = [ pytest ];

  propagatedBuildInputs = [
    dateutil
    rfc3986
    isodate
    uritemplate
  ];
}
