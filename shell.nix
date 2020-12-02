let
  pkgs = import <nixpkgs> {};
  py38WithPackages = pkgs.python38.withPackages (
    ps: with ps; [
      flake8
      graphviz
      jedi
      pynvim
    ]
  );

  sessionToken = pkgs.lib.removeSuffix "\n" (builtins.readFile ./.session_token);
  curl = ''${pkgs.curl}/bin/curl -f --cookie "session=${sessionToken}"'';
  getInputScript = pkgs.writeShellScriptBin "getinput" ''
    [[ $1 == "" ]] && echo "Usage: getinput <day>" && exit 1
    year=$(basename $(pwd))

    outfile=$1
    [[ $(echo "$1 < 10" | bc) == "1" ]] && outfile="0$outfile"

    ${curl} --output $outfile.txt https://adventofcode.com/$year/day/$1/input
  '';

  rg = "${pkgs.ripgrep}/bin/rg --color never";
  printStatsScript = pkgs.writeShellScriptBin "printstats" ''
    year=$(basename $(pwd))

    # Skip if not a year dir
    [[ ! $(echo $year | ${rg} "\d{4}") ]] && exit 0

    ${curl} -s https://adventofcode.com/$year/leaderboard/self |
      ${pkgs.html-xml-utils}/bin/hxselect -c pre |
      ${pkgs.gnused}/bin/sed "s/<[^>]*>//g" |
      ${rg} "^\s*(Day\s+Time|-+Part|\d+\s+(&gt;24h|\d{2}:\d{2}:\d{2}))" |
      ${pkgs.gnused}/bin/sed "s/&gt;/>/g"
  '';

  runScript = pkgs.writeShellScriptBin "run" ''
    day=$1
    [[ $(echo "$1 < 10" | bc) == "1" ]] && day="0$day"

    ${py38WithPackages}/bin/python ./$day.py <./$day.txt
  '';

  # CoC Config
  cocConfig = {
    "python.pythonPath" = "${py38WithPackages}/bin/python";
    "python.jediPath" = "${py38WithPackages}/lib/python3.8/site-packages";
  };
in
pkgs.mkShell {
  # https://e.printstacktrace.blog/merging-json-files-recursively-in-the-command-line/
  shellHook = ''
    mkdir -p .vim
    echo '${builtins.toJSON cocConfig}' |
      ${pkgs.jq}/bin/jq -s \
        'def deepmerge(a;b):
          reduce b[] as $item (a;
            reduce ($item | keys_unsorted[]) as $key (.;
              $item[$key] as $val | ($val | type) as $type | .[$key] = if ($type == "object") then
                deepmerge({}; [if .[$key] == null then {} else .[$key] end, $val])
              elif ($type == "array") then
                (.[$key] + $val | unique)
              else
                $val
              end)
            );
          deepmerge({}; .)' \
        .vim/coc-settings.part.json \
        - \
      > .vim/coc-settings.json
  '';

  POST_CD_COMMAND = "${printStatsScript}/bin/printstats";

  buildInputs = with pkgs; [
    # Core
    rnix-lsp

    # Python
    py38WithPackages
    py38WithPackages.pkgs.flake8
    py38WithPackages.pkgs.yapf

    # Utilities
    getInputScript
    printStatsScript
    runScript
  ];
}
