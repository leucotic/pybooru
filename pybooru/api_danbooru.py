# -*- coding: utf-8 -*-

"""pybooru.api_danbooru

This module contains all API calls of Danbooru for Pybooru.

Classes:
    Danbooru -- Contains all API calls.
"""

# __future__ imports
from __future__ import absolute_import

# pybooru imports
from .exceptions import PybooruAPIError


class DanbooruApi(object):
    """Contains all Danbooru API calls.

    API Versions: v2.105.0
    doc: https://danbooru.donmai.us/wiki_pages/43568
    """

    def post_list(self, **params):
        """Get a list of posts.

        Parameters:
            limit: How many posts you want to retrieve. There is a hard limit
                   of 100 posts per request.
            page: The page number.
            tags: The tags to search for. Any tag combination that works on the
                  web site will work here. This includes all the meta-tags.
            raw: When this parameter is set the tags parameter will not be
                 parsed for aliased tags, metatags or multiple tags, and will
                 instead be parsed as a single literal tag.
        """
        return self._get('posts.json', params)

    def post_show(self, id_):
        """Get a post.

        Parameters:
            id_: REQUIRED Where id_ is the post id.
        """
        return self._get('/posts/{0}.json'.format(id_))

    def post_update(self, id_, tag_string=None, rating=None, source=None,
                    parent_id=None):
        """Update a specific post (Requires login).

        Parameters:
            id_: REQUIRED The id number of the post to update.
            tag_string: A space delimited list of tags.
            rating: The rating for the post. Can be: safe, questionable, or
                    explicit.
            source: If this is a URL, Danbooru will download the file.
            parent_id: The ID of the parent post.
        """
        params = {
            'post[tag_string]': tag_string,
            'post[rating]': rating,
            'ost[source]': source,
            'post[parent_id]': parent_id
            }
        return self._get('/posts/{0}.json'.format(id_), params, 'PUT',
                         auth=True)

    def post_revert(self, id_, version_id):
        """Function to reverts a post to a previous version (Requires login).

        Parameters:
            id_: REQUIRED post id.
            version_id: REQUIRED The post version id to revert to.
        """
        return self._get('/posts/{0}/revert.json'.format(id_),
                         {'version_id': version_id}, 'PUT', auth=True)

    def post_copy_notes(self, id_, other_post_id):
        """Function to copy notes (requires login).

        Parameters:
            id_: REQUIRED Post id.
            other_post_id: REQUIRED The id of the post to copy notes to.
        """
        return self._get('/posts/{0}/copy_notes.json'.format(id_),
                         {'other_post_id': other_post_id}, 'PUT', auth=True)

    def post_vote(self, id_, score):
        """Action lets you vote for a post (Requires login).
        Danbooru: Post votes/create

        Parameters:
            id_: REQUIRED Ppost id.
            score: REQUIRED Can be: up, down.
        """
        return self._get('/posts/{0}/votes.json'.format(id_), {'score': score},
                         'POST', auth=True)

    def post_flag_list(self, creator_id=None, creator_name=None, post_id=None,
                       reason_matches=None, is_resolved=None, category=None):
        """Function to flag a post (Requires login).

        Parameters:
            creator_id: The user id of the flag's creator.
            creator_name: The name of the flag's creator.
            post_id: The post id if the flag.
            reason_matches: Flag's reason.
            is_resolved:
            category: unapproved/banned/normal.
        """
        params = {
            'search[creator_id]': creator_id,
            'search[creator_name]': creator_name,
            'search[post_id]': post_id,
            'search[reason_matches]': reason_matches,
            'search[is_resolved]': is_resolved,
            'search[category]': category
            }
        return self._get('post_flags.json', params, auth=True)

    def post_flag_create(self, id_, reason):
        """Function to flag a post.

        Parameters:
            id_: REQUIRED The id of the flagged post.
            reason: REQUIRED The reason of the flagging.
        """
        params = {'post_flag[post_id]': id_, 'post_flag[reason]': reason}
        return self._get('post_flags.json', params, 'POST', auth=True)

    def post_appeals_list(self, creator_id=None, creator_name=None,
                          post_id=None):
        """Function to return list of appeals (Requires login).

        Parameters:
            creator_id: The user id of the appeal's creator.
            creator_name: The name of the appeal's creator.
            post_id: The post id if the appeal.
        """
        params = {
            'creator_id': creator_id,
            'creator_name': creator_name,
            'post_id': post_id
            }
        return self._get('post_appeals.json', params, auth=True)

    def post_appeals_create(self, id_, reason):
        """Function to create appeals (Requires login).

        Parameters:
            id_: REQUIRED The id of the appealed post.
            reason: REQUIRED The reason of the appeal.
        """
        params = {
            'post_appeal[post_id]': id_,
            'post_appeal[reason]': reason
            }
        return self._get('post_appeals.json', params, 'POST', auth=True)

    def upload_list(self, uploader_id=None, uploader_name=None, source=None):
        """Search and eturn a uploads list (Requires login).

        Parameters:
            uploader_id: The id of the uploader.
            uploader_name: The name of the uploader.
            source The: source of the upload (exact string match).
        """
        params = {
            'search[uploader_id]': uploader_id,
            'search[uploader_name]': uploader_name,
            'search[source]': source
            }
        return self._get('uploads.json', params, auth=True)

    def upload_show(self, upload_id):
        """Get a upload (Requires login).

        Parameters:
            upload_id: Where upload_id is the upload id.
        """
        return self._get('uploads/{0}.json'.format(upload_id), auth=True)

    def upload_create(self, tag_string, rating, file_=None, source=None,
                      parent_id=None):
        """Function to create a new upload (Requires login).

        Parameters:
            tag_string: REQUIRED The tags.
            rating: REQUIRED Can be: safe, questionable, explicit.
            file_: The file data encoded as a multipart form.
            source: The source URL.
            parent_id: The parent post id.
        """
        if file_ or source is not None:
            params = {
                'upload[source]': source,
                'upload[rating]': rating,
                'upload[parent_id]': parent_id,
                'upload[tag_string]': tag_string
                }
            file_ = {'upload[file]': open(file_, 'rb')}
            return self._get('uploads.json', params, 'POST', auth=True,
                             file_=file_)
        else:
            raise PybooruAPIError("'file_' or 'source' is required.")

    def comment_list(self, group_by, body_matches=None, post_id=None,
                     post_tags_match=None, creator_name=None, creator_id=None,
                     tags=None):
        """Return a list of comments.

        Parameters:
            group_by: Can be 'comment', 'post'. Comment will return recent
                      comments. Post will return posts that have been recently
                      commented on.
            The following work only with group_by=comment:
                body_matches: Body contains the given terms.
                post_id: Post id.
                post_tags_match: The comment's post's tags match the given
                                 terms.
                creator_name: The name of the creator (exact match)
                creator_id: The user id of the creator
            The following work only with group_by=post:
                tags The post's tags match the given terms.
        """
        params = {'group_by': group_by}
        if group_by == 'comment':
            params['search[body_matches]'] = body_matches
            params['search[post_id]'] = post_id
            params['search[post_tags_match]'] = post_tags_match
            params['search[creator_name]'] = creator_name
            params['search[creator_id]'] = creator_id
        elif group_by == 'post':
            params['tags'] = tags
        else:
            raise PybooruAPIError("'group_by' must be 'comment' or post")
        return self._get('comments.json', params)

    def comment_create(self, post_id, body, do_not_bump_post=None):
        """Action to lets you create a comment (Requires login).

        Parameters:
            post_id: REQUIRED.
            body: REQUIRED.
            do_not_bump_post: Set to 1 if you do not want the post to be bumped
                              to the top of the comment listing.
        """
        params = {
            'comment[post_id]': post_id,
            'comment[body]': body,
            'comment[do_not_bump_post]': do_not_bump_post
            }
        return self._get('comments.json', params, 'POST', auth=True)

    def comment_update(self, id_, body, do_not_bump_post=None):
        """Function to update a comment (Requires login).

        Parameters:
            id_: REQUIRED comment id.
            body: REQUIRED.
            do_not_bump_post: Set to 1 if you do not want the post to be bumped
                              to the top of the comment listing.
        """
        params = {
            'comment[body]': body,
            'comment[do_not_bump_post]': do_not_bump_post
            }
        return self._get('comments/{0}.json'.format(id_), params, 'PUT',
                         auth=True)

    def comment_show(self, id_):
        """Get a specific comment.

        Parameters:
            id_: REQUIRED the id number of the comment to retrieve.
        """
        return self._get('comments/{0}.json'.format(id_))

    def comment_delete(self, id_):
        """Remove a specific comment (Requires login).

        Parameters:
            id_: REQUIRED the id number of the comment to remove.
        """
        return self._get('comments/{0}.json'.format(id_), method='DELETE',
                         auth=True)

    def favorite_list(self, user_id=None):
        """Return a list with favorite posts (Requires login).

        Parameters:
            user_id: Which user's favorites to show. Defaults to your own if
                     not specified.
        """
        return self._get('favorites.json', {'user_id': user_id}, auth=True)

    def favorite_add(self, post_id):
        """Add post to favorite (Requires login).

        Parameters:
            post_id: REQUIRED The post to favorite.
        """
        return self._get('favorites.json', {'post_id': post_id}, 'POST',
                         auth=True)

    def favorite_remove(self, post_id):
        """Remove a post from favorites (Requires login).

        Parameters:
            post_id: REQUIRED where post_id is the post id.
        """
        return self._get('favorites/{0}.json'.format(post_id), method='DELETE',
                         auth=True)

    def dmail_list(self, message_matches=None, to_name=None, to_id=None,
                   from_name=None, from_id=None, read=None):
        """Return list of Dmails. You can only view dmails you own
        (Requires login).

        Parameters:
            message_matches: The message body contains the given terms.
            to_name: The recipient's name.
            to_id: The recipient's user id.
            from_name: The sender's name.
            from_id: The sender's user id.
            read: Can be: true, false.
        """
        params = {
            'search[message_matches]': message_matches,
            'search[to_name]': to_name,
            'search[to_id]': to_id,
            'search[from_name]': from_name,
            'search[from_id]': from_id,
            'search[read]': read
            }
        return self._get('dmails.json', params, auth=True)

    def dmail_show(self, dmail_id):
        """Return a specific dmail. You can only view dmails you own
        (Requires login).

        Parameters:
            dmail_id: REQUIRED where dmail_id is the dmail id.
        """
        return self._get('dmails/{0}.json'.format(dmail_id), auth=True)

    def dmail_create(self, to_name, title, body):
        """Create a dmail (Requires login)

        Parameters:
            to_name: REQUIRED the recipient's name.
            title: REQUIRED the title of the message.
            body: REQUIRED the body of the message.
        """
        params = {
            'dmail[to_name]': to_name,
            'dmail[title]': title,
            'dmail[body]': body
            }
        return self._get('dmails.json', params, 'POST', auth=True)

    def dmail_delete(self, dmail_id):
        """Delete a dmail. You can only delete dmails you own (Requires login).

        Parameters:
            dmail_id: REQUIRED where dmail_id is the dmail id.
        """
        return self._get('dmails/{0}.json'.format(dmail_id), method='DELETE',
                         auth=True)

    def artist_list(self, query=None, artist_id=None, creator_name=None,
                    creator_id=None, is_active=None, is_banned=None,
                    empty_only=None, order=None):
        """Get an artist of a list of artists.

        Parameters:
            query: This field has multiple uses depending on what the query
                   starts with:
                http: Search for artist with this URL.
                name: Search for artists with the given name as their base
                      name.
                other: Search for artists with the given name in their other
                       names.
                group: Search for artists belonging to the group with the given
                       name.
                status:banned Search for artists that are banned.
                else Search for the given name in the base name and the other
                     names.
            artist_id: The artist id.
            creator_name:
            creator_id:
            is_active: Can be: true, false
            is_banned: Can be: true, false
            empty_only: Search for artists that have 0 posts. Can be: true
            order: Can be: name, updated_at.
        """
        params = {
            'search[name]': query,
            'search[id]': artist_id,
            'search[creator_name]': creator_name,
            'search[creator_id]': creator_id,
            'search[is_active]': is_active,
            'search[is_banned]': is_banned,
            'search[empty_only]': empty_only,
            'search[order]': order
            }
        return self._get('artists.json', params)

    def artist_show(self, artist_id):
        """Return a specific artist.

        Parameters:
            artist_id: REQUIRED where artist_id is the artist id.
        """
        return self._get('artists/{0}.json'.format(artist_id))

    def artist_create(self, name, other_names_comma=None, group_name=None,
                      url_string=None):
        """Function to create an artist (Requires login) (UNTESTED).

        Parameters:
            name: REQUIRED.
            other_names_comma: List of alternative names for this artist, comma
                               delimited.
            group_name: The name of the group this artist belongs to.
            url_string: List of URLs associated with this artist, whitespace or
                        newline delimited.
        """
        params = {
            'artist[name]': name,
            'artist[other_names_comma]': other_names_comma,
            'artist[group_name]': group_name,
            'artist[url_string]': url_string
            }
        return self.get('artists.json', params, method='POST', auth=True)

    def artist_update(self, artist_id, name=None, other_names_comma=None,
                      group_name=None, url_string=None):
        """Function to update artists (Requires login) (UNTESTED).

        Parameters:
            artist_id: REQUIRED where artist_id is the artist id.
            name:
            other_names_comma: List of alternative names for this artist, comma
                               delimited.
            group_name: The name of the group this artist belongs to.
            url_string: List of URLs associated with this artist, whitespace or
                        newline delimited.
        """
        params = {
            'artist[name]': name,
            'artist[other_names_comma]': other_names_comma,
            'artist[group_name]': group_name,
            'artist[url_string]': url_string
            }
        return self .get('artists/{0}.json'.format(artist_id), params,
                         method='PUT', auth=True)

    def artist_delete(self, artist_id):
        """Action to lets you delete an artist (Requires login) (UNTESTED).

        Parameters:
            artist_id: where artist_id is the artist id.
        """
        return self._get('artists/{0}.json'.format(artist_id), method='DELETE',
                         auth=True)

    def artist_banned(self):
        """This is a shortcut for an artist listing search with
        name=status:banned.
        """
        return self._get('artists/banned.json')

    def artist_revert(self, artist_id, version_id):
        """Revert an artist (Requires login) (UNTESTED).

        Parameters:
            artist_id: REQUIRED The artist id.
            version_id: REQUIRED The artist version id to revert to.
        """
        params = {'version_id': version_id}
        return self._get('artists/{0}/revert.json'.format(artist_id), params,
                         method='PUT', auth=True)

    def note_list(self, group_by=None, body_matches=None, post_id=None,
                  post_tags_match=None, creator_name=None, creator_id=None):
        """Return list of notes.

        Parameters:
            group_by: Can be: note, post (by default post).
            body_matches: The note's body matches the given terms.
            post_id: A specific post.
            post_tags_match: The note's post's tags match the given terms.
            creator_name: The creator's name. Exact match.
            creator_id: The creator's user id.
        """
        params = {
            'group_by': group_by,
            'search[body_matches]': body_matches,
            'search[post_id]': post_id,
            'search[post_tags_match]': post_tags_match,
            'search[creator_name]': creator_name,
            'search[creator_id]': creator_id
            }
        return self._get('notes.json', params)

    def note_show(self, note_id):
        """Get a specific note.

        Parameters:
            note_id: REQUIRED Where note_id is the note id.
        """
        return self._get('notes/{0}.json'.format(note_id))

    def note_create(self, post_id, coor_x, coor_y, width, height, body):
        """Function to create a note (Requires login) (UNTESTED).

        Parameters:
            post_id: REQUIRED
            coor_x: REQUIRED The x coordinates of the note in pixels, with
                    respect to the top-left corner of the image.
            coor_y: REQUIRED The y coordinates of the note in pixels, with
                    respect to the top-left corner of the image.
            width: REQUIRED The width of the note in pixels.
            height: REQUIRED The height of the note in pixels.
            body: REQUIRED The body of the note.
        """
        params = {
            'note[post_id]': post_id,
            'note[x]': coor_x,
            'note[y]': coor_y,
            'note[width]': width,
            'note[height]': height,
            'note[body]': body
            }
        return self._get('notes.json', params, method='POST', auth=True)

    def note_update(self, note_id, coor_x=None, coor_y=None, width=None,
                    height=None, body=None):
        """Function to update a note (Requires login) (UNTESTED).

        Parameters:
            note_id: REQUIRED Where note_id is the note id.
            coor_x: REQUIRED The x coordinates of the note in pixels, with
                    respect to the top-left corner of the image.
            coor_y: REQUIRED The y coordinates of the note in pixels, with
                    respect to the top-left corner of the image.
            width: REQUIRED The width of the note in pixels.
            height: REQUIRED The height of the note in pixels.
            body: REQUIRED The body of the note.
        """
        params = {
            'note[x]': coor_x,
            'note[y]': coor_y,
            'note[width]': width,
            'note[height]': height,
            'note[body]': body
            }
        return self._get('notes/{0}.jso'.format(note_id), params, method='PUT',
                         auth=True)
