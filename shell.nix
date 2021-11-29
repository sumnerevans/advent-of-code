let
  pkgs = import <nixpkgs> {
    overlays = [
      (self: super: {
        pypy3 = super.pypy3.override {
          sourceVersion = {
            major = "7";
            minor = "3";
            patch = "7";
          };
          sha256 = "sha256-Ia4zn09QFtbKcwAwXz47VUNzg1yzw5qQQf4w5oEcgMY=";
          pythonVersion = "3.8";
        };
      })
    ];
  };
  py3WithPackages = pkgs.python3.withPackages (
    ps: with ps; [
      black
      flake8
      graphviz
      pynvim
    ]
  );

  curl = ''${pkgs.curl}/bin/curl -f --cookie "session=$sessionToken"'';
  rg = "${pkgs.ripgrep}/bin/rg --color never";
  getInputScript = pkgs.writeShellScriptBin "getinput" ''
    [[ $1 == "" ]] && echo "Usage: getinput <day>" && exit 1
    year=$(basename $(pwd))

    # Error if not a year dir
    [[ ! $(echo $year | ${rg} "\d{4}") ]] && echo "Not a year dir" && exit 1

    outfile=$1
    [[ $(echo "$1 < 10" | ${pkgs.bc}/bin/bc) == "1" ]] && outfile="0$outfile"

    mkdir -p inputs
    sessionToken=$(cat ${builtins.getEnv "PWD"}/.session_token)
    ${curl} --output inputs/$outfile.txt https://adventofcode.com/$year/day/$1/input

    less inputs/$outfile.txt
  '';

  printStatsScript = pkgs.writeShellScriptBin "printstats" ''
    year=$(basename $(pwd))

    # Skip if not a year dir
    [[ ! $(echo $year | ${rg} "\d{4}") ]] && exit 0

    sessionToken=$(cat ${builtins.getEnv "PWD"}/.session_token)
    ${curl} -s https://adventofcode.com/$year/leaderboard/self |
      ${pkgs.html-xml-utils}/bin/hxselect -c pre |
      ${pkgs.gnused}/bin/sed "s/<[^>]*>//g" |
      ${rg} "^\s*(Day\s+Time|-+Part|\d+\s+(&gt;24h|\d{2}:\d{2}:\d{2}))" |
      ${pkgs.gnused}/bin/sed "s/&gt;/>/g"
  '';

  getDayScriptPart = scriptName: ''
    # Check that day is passed in.
    [[ $1 == "" ]] && echo "Usage: ${scriptName} <day>" && exit 1
    day=$1

    # Error if no day
    [[ ! $(echo $day | ${rg} "\d+") ]] && echo "Not a valid day" && exit 1

    # Zero-pad day
    [[ $(echo "$1 < 10" | ${pkgs.bc}/bin/bc) == "1" ]] && day="0$day"
  '';

  runScript = pkgs.writeShellScriptBin "run" ''
    ${getDayScriptPart "run"}

    ${pkgs.watchexec}/bin/watchexec -r "${pkgs.pypy3}/bin/pypy3 ./$day.py"
  '';

  debugRunScript = pkgs.writeShellScriptBin "drun" ''
    ${getDayScriptPart "drun"}

    ${pkgs.watchexec}/bin/watchexec -r "${pkgs.pypy3}/bin/pypy3 ./$day.py --debug"
  '';

  # Single run, don't watchexec
  singleRunScript = pkgs.writeShellScriptBin "srun" ''
    ${getDayScriptPart "srun"}

    ${pkgs.pypy3}/bin/pypy3 ./$day.py
  '';

  debugSingleRunTestScript = pkgs.writeShellScriptBin "dsrun" ''
    ${getDayScriptPart "dsrun"}

    ${pkgs.pypy3}/bin/pypy3 ./$day.py --debug
  '';

  # Write a test file
  mkTestScript = pkgs.writeShellScriptBin "mktest" ''
    ${getDayScriptPart "mktest"}
    ${pkgs.xsel}/bin/xsel --output > inputs/$day.test.txt
  '';

  # Run with --test flag
  runTestScript = pkgs.writeShellScriptBin "runtest" ''
    ${getDayScriptPart "runtest"}
    ${pkgs.pypy3}/bin/pypy3 ./$day.py --test
  '';

  debugRunTestScript = pkgs.writeShellScriptBin "druntest" ''
    ${getDayScriptPart "druntest"}
    ${pkgs.pypy3}/bin/pypy3 ./$day.py --test --debug
  '';

  # Run with --stdin flag
  runStdinScript = pkgs.writeShellScriptBin "runstdin" ''
    ${getDayScriptPart "runstdin"}
    ${pkgs.pypy3}/bin/pypy3 ./$day.py --stdin
  '';

  # Compile and run the C version.
  cRunScript = pkgs.writeShellScriptBin "crun" ''
    ${getDayScriptPart "crun"}
    mkdir -p bin
    gcc -o bin/$day $day.c
    ./bin/$day
  '';

  cRunTestScript = pkgs.writeShellScriptBin "cruntest" ''
    ${getDayScriptPart "cruntest"}
    mkdir -p bin
    gcc -o bin/$day $day.c
    ./bin/$day --test
  '';

  # CoC Config
  cocConfig = pkgs.writeText "coc-settings.json" (
    builtins.toJSON {
      "python.formatting.provider" = "black";
      "python.linting.flake8Enabled" = true;
      "python.linting.mypyEnabled" = true;
      "python.linting.pylintEnabled" = false;
      "python.pythonPath" = "${py3WithPackages}/bin/python";
      "clangd.path" = "${pkgs.clang-tools}/bin/clangd";
    }
  );
in
pkgs.mkShell {
  shellHook = ''
    mkdir -p .vim
    ln -sf ${cocConfig} .vim/coc-settings.json
  '';

  POST_CD_COMMAND = "${printStatsScript}/bin/printstats";

  buildInputs = with pkgs; [
    # Core
    coreutils
    gnumake
    rnix-lsp
    sloccount
    tokei

    # C/C++
    clang
    gcc
    gdb
    valgrind

    # Python
    py3WithPackages
    py3WithPackages.pkgs.black
    py3WithPackages.pkgs.flake8
    pypy3

    # Utilities
    cRunScript
    cRunTestScript
    debugRunScript
    debugRunTestScript
    debugSingleRunTestScript
    getInputScript
    mkTestScript
    printStatsScript
    runScript
    runStdinScript
    runTestScript
    singleRunScript
  ];
}
