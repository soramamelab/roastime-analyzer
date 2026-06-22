#!/bin/bash
set -e

cd "$(dirname "$0")"

VERSION=$(awk -F': ' '/^Version:/{print $2}' debian/control)
PKG_NAME="roastime-analyzer_${VERSION}_all"
PKG_DIR="dist/${PKG_NAME}"

echo "== ビルドディレクトリを準備しています =="
rm -rf "dist/${PKG_NAME}"
mkdir -p "$PKG_DIR/DEBIAN"
mkdir -p "$PKG_DIR/opt/roastime-analyzer"
mkdir -p "$PKG_DIR/usr/bin"
mkdir -p "$PKG_DIR/usr/share/applications"
mkdir -p "$PKG_DIR/usr/share/doc/roastime-analyzer"

echo "== アプリ本体を配置しています =="
cp app.py requirements.txt "$PKG_DIR/opt/roastime-analyzer/"

echo "== パッケージメタ情報を配置しています =="
cp debian/control debian/postinst debian/postrm "$PKG_DIR/DEBIAN/"
chmod 755 "$PKG_DIR/DEBIAN/postinst" "$PKG_DIR/DEBIAN/postrm"

cp debian/roastime-analyzer "$PKG_DIR/usr/bin/roastime-analyzer"
chmod 755 "$PKG_DIR/usr/bin/roastime-analyzer"

cp debian/roastime-analyzer.desktop "$PKG_DIR/usr/share/applications/"
cp debian/copyright "$PKG_DIR/usr/share/doc/roastime-analyzer/copyright"

echo "== パーミッションを整えています =="
find "$PKG_DIR" -mindepth 1 -not -path "$PKG_DIR/DEBIAN*" -type d -exec chmod 755 {} +
find "$PKG_DIR/opt" "$PKG_DIR/usr/share" -type f -exec chmod 644 {} +
chmod 755 "$PKG_DIR/usr/bin/roastime-analyzer"

echo "== .deb をビルドしています =="
dpkg-deb --build --root-owner-group "$PKG_DIR"

echo ""
echo "ビルド完了: dist/${PKG_NAME}.deb"
