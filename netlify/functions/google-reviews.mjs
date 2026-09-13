const responseHeaders={
  'Content-Type':'application/json; charset=utf-8',
  'Cache-Control':'private, no-store, max-age=0',
  'X-Content-Type-Options':'nosniff'
};

const json=(body,status=200)=>new Response(JSON.stringify(body),{status,headers:responseHeaders});

const safeHttpsUrl=value=>{
  if(typeof value!=='string')return '';
  try{
    const url=new URL(value);
    return url.protocol==='https:'?url.href:'';
  }catch{return ''}
};

const finiteNumber=value=>Number.isFinite(Number(value))?Number(value):null;

export default async request=>{
  if(request.method!=='GET')return json({error:'method_not_allowed'},405);

  const apiKey=process.env.GOOGLE_PLACES_API_KEY;
  const placeId=process.env.GOOGLE_PLACE_ID;
  if(!apiKey||!placeId)return json({error:'google_reviews_not_configured'},503);

  const endpoint=new URL(`https://places.googleapis.com/v1/places/${encodeURIComponent(placeId)}`);
  endpoint.searchParams.set('languageCode','he');
  endpoint.searchParams.set('regionCode','IL');

  let googleResponse;
  try{
    googleResponse=await fetch(endpoint,{
      headers:{
        'Accept':'application/json',
        'X-Goog-Api-Key':apiKey,
        'X-Goog-FieldMask':'displayName,rating,userRatingCount,reviews,googleMapsLinks,attributions'
      },
      signal:AbortSignal.timeout(8000)
    });
  }catch(error){
    console.error('Google Places request failed:',error.name);
    return json({error:'google_places_unavailable'},502);
  }

  if(!googleResponse.ok){
    console.error('Google Places returned status:',googleResponse.status);
    return json({error:'google_places_error'},502);
  }

  const place=await googleResponse.json();
  const links=place.googleMapsLinks||{};
  const reviews=(Array.isArray(place.reviews)?place.reviews:[]).map(review=>{
    const author=review.authorAttribution||{};
    const translatedLanguage=review.text?.languageCode||'';
    const originalLanguage=review.originalText?.languageCode||'';
    return {
      authorName:String(author.displayName||'משתמש Google'),
      authorUri:safeHttpsUrl(author.uri),
      authorPhotoUri:safeHttpsUrl(author.photoUri),
      rating:finiteNumber(review.rating),
      relativeTime:String(review.relativePublishTimeDescription||''),
      text:String(review.text?.text||review.originalText?.text||''),
      isTranslated:Boolean(translatedLanguage&&originalLanguage&&translatedLanguage!==originalLanguage),
      reviewUri:safeHttpsUrl(review.googleMapsUri),
      flagContentUri:safeHttpsUrl(review.flagContentUri)
    };
  });

  const attributions=(Array.isArray(place.attributions)?place.attributions:[]).map(attribution=>({
    provider:String(attribution.provider||''),
    providerUri:safeHttpsUrl(attribution.providerUri)
  })).filter(attribution=>attribution.provider);

  return json({
    name:String(place.displayName?.text||''),
    rating:finiteNumber(place.rating),
    reviewCount:finiteNumber(place.userRatingCount),
    placeUri:safeHttpsUrl(links.placeUri),
    reviewsUri:safeHttpsUrl(links.reviewsUri),
    writeReviewUri:safeHttpsUrl(links.writeAReviewUri),
    reviews,
    attributions
  });
};
