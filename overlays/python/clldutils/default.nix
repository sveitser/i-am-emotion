{ buildPythonPackage
, fetchPypi
, attrs
, dateutil
, colorlog
, tabulate
, configparser
, csvw
}:

buildPythonPackage rec {

  pname = "clldutils";
  version = "2.6.3";

  src = fetchPypi {
    inherit pname version;
    sha256 = "0g8a7kwzsjqp05dci3kz8k13ildwcgvhfdjwk0z57bm0pngzfygl";
  };

  propagatedBuildInputs = [
    attrs
    dateutil
    colorlog
    tabulate
    configparser
    csvw
  ];
}
