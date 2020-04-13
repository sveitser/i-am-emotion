with import <nixpkgs> {};

mkShell {
  buildInputs = [
    hivemind
  ];
  shellHook = ''
    export PATH=$(pwd)/bin:$PATH
  '';
}
