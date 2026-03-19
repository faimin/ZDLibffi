#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

LIBFFI_VERSION="3.5.2"
POD_VERSION=""
SKIP_XCFRAMEWORK=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --libffi-version)
      LIBFFI_VERSION="$2"
      shift 2
      ;;
    --pod-version)
      POD_VERSION="$2"
      shift 2
      ;;
    --skip-xcframework)
      SKIP_XCFRAMEWORK=1
      shift
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if [[ -z "${POD_VERSION}" ]]; then
  POD_VERSION="0.${LIBFFI_VERSION//./}.0"
fi

WORK_DIR="$(mktemp -d "${TMPDIR:-/tmp}/zdlibffi-upgrade.XXXXXX")"
trap 'rm -rf "${WORK_DIR}"' EXIT

ARCHIVE_NAME="libffi-${LIBFFI_VERSION}.tar.gz"
LIBFFI_DIR="${WORK_DIR}/libffi-${LIBFFI_VERSION}"
DOWNLOAD_URL="https://github.com/libffi/libffi/releases/download/v${LIBFFI_VERSION}/${ARCHIVE_NAME}"

printf 'Downloading %s\n' "${DOWNLOAD_URL}"
curl -fL "${DOWNLOAD_URL}" -o "${WORK_DIR}/${ARCHIVE_NAME}"

tar -xzf "${WORK_DIR}/${ARCHIVE_NAME}" -C "${WORK_DIR}"

python3 "${SCRIPT_DIR}/prepare_libffi_source.py" \
  --libffi-dir "${LIBFFI_DIR}" \
  --output "${REPO_ROOT}/Source"

if [[ "${SKIP_XCFRAMEWORK}" -eq 0 ]]; then
  python3 "${SCRIPT_DIR}/build_xcframework.py" \
    --source "${REPO_ROOT}/Source" \
    --output "${REPO_ROOT}/XCFramework/ZDLibffi.xcframework" \
    --build-dir "${REPO_ROOT}/build/xcframework"
fi

perl -0777 -i -pe "s/s\.version\s*=\s*'[^']+'/s.version          = '${POD_VERSION}'/; s/libffi v[0-9]+\.[0-9]+\.[0-9]+ integrate/libffi v${LIBFFI_VERSION} integrate/g" "${REPO_ROOT}/ZDLibffi.podspec"
perl -0777 -i -pe "s/libffi v[0-9]+\.[0-9]+\.[0-9]+/libffi v${LIBFFI_VERSION}/g" "${REPO_ROOT}/README.md"

echo "Upgrade complete: libffi ${LIBFFI_VERSION}, pod version ${POD_VERSION}."
if [[ "${SKIP_XCFRAMEWORK}" -eq 0 ]]; then
  echo "XCFramework generated at XCFramework/ZDLibffi.xcframework"
fi
