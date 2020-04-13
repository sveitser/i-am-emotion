with import ./nix/nixpkgs.nix {};

let
  py = python36;
in
mkShell {

  SOURCE_DATE_EPOCH = "315532800";

  buildInputs = [
    entr
    portaudio

    py.pkgs.pip
    py.pkgs.setuptools
    py.pkgs.pyaudio
    hivemind
  ];

  shellHook = ''
      export PIP_PREFIX="$(pwd)/.build/pip_packages"
      export PATH="$PIP_PREFIX/bin:$PATH"
      export PYTHONPATH="$PIP_PREFIX/${py.sitePackages}:$PYTHONPATH"
      unset SOURCE_DATE_EPOCH
  '';
}
