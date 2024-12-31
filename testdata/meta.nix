{
  pkgs,
  lib,
  config,
  inputs,
  ...
}: {
  name = "devenvls";

  languages = {
    go.enable = true;
    nix.enable = true;
  };

  packages = with pkgs; [
    git
    podman
    zsh
    iferr
    go
    gopls
    impl
    golangci-lint-langserver
    golangci-lint
    revive
    gomodifytags
    gotests
    gotools
    gomarkdoc
  ];

  scripts = {
    generate.exec = ''
      go generate -v ./...
    '';
    run.exec = ''
      go run main.go
    '';
    dx.exec = ''
      $EDITOR $(git rev-parse --show-toplevel)/devenv.nix
    '';
  };

  enterShell = ''
    git status
  '';

  # https://devenv.sh/tests/
  enterTest = ''
    echo "Running tests"
    git --version | grep --color=auto "${pkgs.git.version}"
  '';

  cachix.enable = true;
}
