<?php

add_filter( "mwai_context_search", 'my_web_search', 10, 3 );

function my_web_search( $context, $query, $options = [] ) {
  // If the context is already provided, return it as is.
  if ( ! empty( $context ) ) {
    return $context;
  }

  // Get the latest question from the visitor.
  $lastMessage = $query->getLastMessage();

  // Perform a search via the Google Custom Search API.
  $apiKey = 'YOUR_API_KEY';
  $engineId = 'YOUR_ENGINE_ID';
  if ( empty( $apiKey ) || empty( $engineId ) ) {
    return null;
  }
  $url = "https://www.googleapis.com/customsearch/v1?key=$apiKey&cx=$engineId&q=" . urlencode( $lastMessage );
  $response = wp_remote_get( $url );
  if ( is_wp_error( $response ) ) {
    return null;
  }
  $body = wp_remote_retrieve_body( $response );
  $data = json_decode( $body );
  if ( empty( $data->items ) ) {
    return null;
  }

  // AI Engine expects a type (for logging purposes) and the content (which will be used by AI).
  $context["type"] = "websearch";
  $context["content"] = "";

  // Loop through the 5 first results.
  $max = min( count( $data->items ), 5 );
  for ( $i = 0; $i < $max; $i++ ) {
    $result = $data->items[$i];
    $title = $result->title;
    $url = $result->link;
    $snippet = $result->snippet;
    $content = "Title: $title\nExcerpt: $snippet\nURL: $url\n\n";
    $context["content"] .= $content;
  }

  return $context;
}
