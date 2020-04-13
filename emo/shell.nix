with import (
  builtins.fetchTarball {
   url = "https://github.com/nixos/nixpkgs/archive/d9f7d27ef54188158311fb787c273afd7d8e5f12.tar.gz";
   sha256 = "0fhg2mc6nrqdwp8d69nfcl3aj7l6bw6x8c30yf40jpgf4c301jxs";
  }) {
  overlays = [
    (self: super:
      if super.stdenv.isDarwin
      then {}
      else {
        opencv3 = super.opencv3.override (old: {
          enableGtk2 = true;
        });
      }
    )
  ];
};

let mss = python3Packages.buildPythonPackage rec {
  pname = "mss";
  version = "3.3.2";
  src = python3Packages.fetchPypi {
    inherit pname version;
    sha256 = "1si2n0n4xa431g5as3s19hgk5x5621jbqm4lm21drz2iz3r9v849";
  };
  # Imports windows specific stuff. Fails.
  doCheck = false;
};
in
mkShell {

  buildInputs = [
    (python36.withPackages (ps: with ps; [
      jupyterlab   # notebooks
      matplotlib   # make charts (pretty low level)
      pandas       # data frames
      pillow       # image manipulation
      scikitlearn  # machine learning
      seaborn      # prettier charts
      tensorflow   # deep learning
      Keras        # tensorflow for humans
      opencv3      # computer vision tools
      mss          # capture scren
      flask        # backend
      
      gunicorn
    ]))
  ] ++ (if stdenv.isDarwin then [] else [ gtk2-x11 ]);

  shellHook = ''
    export PYTHONPATH=src
  '';

}
