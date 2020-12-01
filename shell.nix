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
  getInputScript = pkgs.writeShellScriptBin "getinput" ''
    [[ $1 == "" ]] && echo "Usage: getinput <day>" && exit 1
    year=$(basename $(pwd))

    outfile=$1
    [[ $(echo "$1 < 10" | bc) == "1" ]] && outfile="0$outfile"

    ${pkgs.curl}/bin/curl \
        -f \
        --cookie "session=${sessionToken}" \
        --output $outfile.txt \
        https://adventofcode.com/$year/day/$1/input
  '';

  # CoC Config
  cocConfig = {
    "python.pythonPath" = "${py38WithPackages}/bin/python";
    "python.jediPath" = "${py38WithPackages}/lib/python3.8/site-packages";
  };
in
pkgs.mkShell {
  shellHook = ''
    # https://e.printstacktrace.blog/merging-json-files-recursively-in-the-command-line/
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

  buildInputs = with pkgs; [
    # Core
    rnix-lsp

    # Python
    py38WithPackages
    py38WithPackages.pkgs.flake8
    py38WithPackages.pkgs.yapf

    # Utilities
    getInputScript
  ];
}
