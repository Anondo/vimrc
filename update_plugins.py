import zipfile
import shutil
import tempfile
import requests

from os import path

requests.packages.urllib3.disable_warnings()

#--- Globals ----------------------------------------------
PLUGINS = """
bufexplorer https://github.com/corntrace/bufexplorer
ctrlp.vim https://github.com/kien/ctrlp.vim
delimitMate https://github.com/Raimondi/delimitMate
emmet-vim https://github.com/mattn/emmet-vim
go-explorer https://github.com/garyburd/go-explorer
goyo.vim https://github.com/junegunn/goyo.vim
gundo.vim https://github.com/sjl/gundo.vim
limelight.vim https://github.com/junegunn/limelight.vim
matchit https://github.com/tmhedberg/matchit
mayansmoke https://github.com/vim-scripts/mayansmoke
mru https://github.com/yegappan/mru
nerdcommenter https://github.com/scrooloose/nerdcommenter
nerdtree https://github.com/scrooloose/nerdtree
nginx.vim https://github.com/vim-scripts/nginx.vim
open_file_under_cursor.vim https://github.com/amix/open_file_under_cursor.vim
peaksea https://github.com/vim-scripts/peaksea
php.vim https://github.com/StanAngeloff/php.vim
python-mode https://github.com/klen/python-mode
rainbow_parentheses.vim https://github.com/kien/rainbow_parentheses.vim
rust.vim https://github.com/rust-lang/rust.vim
snipmate-snippets https://github.com/scrooloose/snipmate-snippets
syntastic https://github.com/scrooloose/syntastic
tagbar https://github.com/majutsushi/tagbar
taglist.vim https://github.com/vim-scripts/taglist.vim
tlib https://github.com/vim-scripts/tlib
typescript-vim https://github.com/leafgarland/typescript-vim
unite.vim https://github.com/Shougo/unite.vim
ultisnips https://github.com/sirver/ultisnips
vim-abolish https://github.com/tpope/vim-abolish
vim-addon-mw-utils https://github.com/MarcWeber/vim-addon-mw-utils
vim-airline https://github.com/vim-airline/vim-airline
vim-airline-themes https://github.com/vim-airline/vim-airline-themes
vim-blade https://github.com/xsbeats/vim-blade
vim-bundle-mako https://github.com/sophacles/vim-bundle-mako
vim-clojure-highlight https://github.com/guns/vim-clojure-highlight
vim-clojure-static https://github.com/guns/vim-clojure-static
vim-coffee-script https://github.com/kchmck/vim-coffee-script
vim-coloresque https://github.com/gorodinskiy/vim-coloresque
vim-colors-solarized https://github.com/altercation/vim-colors-solarized
vim-easymotion https://github.com/Lokaltog/vim-easymotion
vim-expand-region https://github.com/terryma/vim-expand-region
vim-eunuch https://github.com/tpope/vim-eunuch
vim-fireplace https://github.com/tpope/vim-fireplace
vim-fugitive https://github.com/tpope/vim-fugitive
vim-go https://github.com/fatih/vim-go
vim-gitgutter https://github.com/airblade/vim-gitgutter
vim-hy https://github.com/hylang/vim-hy
vim-indent-guides https://github.com/nathanaelkane/vim-indent-guides
vim-indent-object https://github.com/michaeljsmith/vim-indent-object
vim-javascript https://github.com/pangloss/vim-javascript
vim-javascript-syntax https://github.com/jelera/vim-javascript-syntax
vim-jsbeautify https://github.com/maksimr/vim-jsbeautify
vim-jsx https://github.com/mxw/vim-jsx
vim-less https://github.com/groenewege/vim-less
vim-markdown https://github.com/tpope/vim-markdown
vim-multiple-cursors https://github.com/terryma/vim-multiple-cursors
vim-pyte https://github.com/therubymug/vim-pyte
vim-repeat https://github.com/tpope/vim-repeat
vim-sexp https://github.com/guns/vim-sexp
vim-sexp-mappings-for-regular-people https://github.com/tpope/vim-sexp-mappings-for-regular-people
vim-speeddating https://github.com/tpope/vim-speeddating
vim-surround https://github.com/tpope/vim-surround
vim-zenroom2 https://github.com/amix/vim-zenroom2
""".strip()

GITHUB_ZIP = '%s/archive/master.zip'

SOURCE_DIR = path.join( path.dirname(__file__), 'sources_non_forked' )


def download_extract_replace(plugin_name, zip_path, temp_dir, source_dir):
    temp_zip_path = path.join(temp_dir, plugin_name)

    # Download and extract file in temp dir
    req = requests.get(zip_path)
    open(temp_zip_path, 'wb').write(req.content)

    zip_f = zipfile.ZipFile(temp_zip_path)
    zip_f.extractall(temp_dir)

    plugin_temp_path = path.join(temp_dir,
    path.join(temp_dir, '%s-master' % plugin_name))

    # Remove the current plugin and replace it with the extracted
    plugin_dest_path = path.join(source_dir, plugin_name)

    try:
        shutil.rmtree(plugin_dest_path)
    except OSError:
        pass

    shutil.move(plugin_temp_path, plugin_dest_path)

    print 'Updated %s' % plugin_name


if __name__ == '__main__':
    temp_directory = tempfile.mkdtemp()

    try:
        for line in PLUGINS.splitlines():
            name, github_url = line.split(' ')
            zip_path = GITHUB_ZIP % github_url
            download_extract_replace(name, zip_path,
            temp_directory, SOURCE_DIR)
    finally:
        shutil.rmtree(temp_directory)
