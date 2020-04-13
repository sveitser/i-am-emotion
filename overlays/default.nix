with import <nixpkgs> {
  overlays = [ (import ./python.nix) ];
};

(python3.withPackages (ps: with ps; [
  clldutils
  csvw
  horovod
  joblib
  lws
  phonemizer
  resampy
  segments
  tensorboardX
]))

