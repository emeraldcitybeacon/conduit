Conformance and Profiles
=========================

The goal of HSDS is to provide a common model for Human Services data, so that it MAY be consumed and used consistently by humans and systems. Therefore we set out these principles for conforming to the standard.

The nature of Human Services inevitably results in variations between different local or regional contexts. HSDS accounts for this by explicitly creating space for different **Profiles** of HSDS to respond to local needs.

## Conformance Specifications

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED",  "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119).

A publication MAY be conformant either to HSDS as specified by this reference or to a HSDS Profile.

### Conformance with HSDS

1. A publication conforming to HSDS MAY only use a subset of this specifications terms.
2. It MUST NOT use terms outside of this specification where terms from this specification would suffice.
3. It MUST use terms from this specification in a manner that is consistent with the semantics of those terms as defined in this specification.
4. It MAY use terms from outside of this specification where this specification's terms are insufficient.[^additional-fields]
5. If the publication serializes to JSON, then it MUST validate against the this specification's [JSON Schemas](https://github.com/openreferral/specification/tree/3.0/schema).

(The above was inspired by the [Popolo Project](https://www.popoloproject.com/specs/#conformance)'s conformance section)

In lay terms, this can be interpreted as the following:

* A HSDS publication doesn't have to contain all properties specified in HSDS; publishers can omit non-required properties.
* A HSDS publication shouldn't use any additional or non-HSDS properties when there's an existing HSDS property available that is suitable.
* A HSDS publication has to use HSDS properties in the way that these properties were intended, as specified by the semantic definitions of these properties in HSDS.
* A HSDS publication can use additional non-HSDS properties where there's no existing HSDS properties that are suitable.
* The data inside a HSDS JSON publication has to validate against the JSON Schemas which define HSDS.

[^additional-fields]: The [HSDS schemas](schema_reference) allow for the inclusion of new properties by default and will not fail validation of a file which contains unknown properties. This can sometimes be known as [Extending the Schema](extending).

### Conformance with a HSDS Profile

HSDS Profiles provide a method of building upon and tailoring the core HSDS Schema in order to adapt it for specific contexts which MAY require different or additional validation rules. Therefore a publication MAY conform to a HSDS Profile rather than HSDS itself.

Each Profile's specification and rules are different, so we outline the high-level rules for conformance to a HSDS Profile here.

1. A publication conforming to a HSDS Profile MUST declare the canonical URI of the Profile as specified in the [API Specification](https://github.com/openreferral/specification/blob/3.0/schema/openapi.json).
2. A publication conforming to a HSDS Profile MAY only use a subset of that Profile's specified terms.
3. It MUST NOT use terms outside of that Profile's specification where terms from the Profile's specification would suffice.
4. It MUST use terms from the Profile's specification in a manner that is consistent with the semantics of those terms defined in the Profile.
5. It MAY use terms from outside of the Profile's specification where the terms provided in the Profile's specification are insufficient.
6. If the publication serializes to JSON then it MUST validate against the Profile's JSON Schemas.

For more information on HSDS Profiles, please see [Using Profiles](using_profiles) in the Guidance section.
