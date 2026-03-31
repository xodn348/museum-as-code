# API Samples Directory

This directory contains sample API responses from the e뮤지엄 Open API.

## Files

| File | Description |
|------|-------------|
| `emuseum_relic_list_sample.xml` | Sample response from `/relic/list` endpoint showing 3 national treasures |
| `emuseum_relic_detail_sample.xml` | Sample response from `/relic/detail` endpoint with full artifact info |
| `emuseum_code_list_sample.xml` | Sample response from `/code` endpoint showing museum codes |

## Important Notes

1. **Authentication Required**: These are mock samples. Real API calls require a valid `serviceKey` from 공공데이터포털.

2. **Response Format**: API returns XML by default. Use `Accept: application/json` header for JSON.

3. **Key Fields**:
   - `id`: Unique artifact identifier
   - `crltsNm`: Artifact name (Korean)
   - `ccbaKdcd`: Classification code (11=국보, 12=보물)
   - `ccbaAsno`: Serial number
   - `imgUrl`: Primary image URL

4. **Image URLs**: Images are served from `https://www.emuseum.go.kr/thumb/` with a specific path structure based on the artifact ID.

## Usage

These samples are used for:
- Testing pipeline data transformation logic
- Understanding API response structure
- Developing parsers without making actual API calls

## See Also

- [API_MAPPING.md](../API_MAPPING.md) - Full API documentation and field mapping
- [pipeline/README.md](../README.md) - Pipeline overview
