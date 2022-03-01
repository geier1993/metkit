/*
 * (C) Copyright 2017- ECMWF.
 *
 * This software is licensed under the terms of the Apache Licence Version 2.0
 * which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
 * In applying this licence, ECMWF does not waive the privileges and immunities
 * granted to it by virtue of its status as an intergovernmental organisation nor
 * does it submit to any jurisdiction.
 */

/// @author Baudouin Raoult
/// @date   Jun 2020

#include "metkit/codes/BufrContent.h"

#include "eckit/exception/Exceptions.h"
#include "eckit/memory/Zero.h"

#include "metkit/codes/GribHandle.h"

namespace metkit {
namespace codes {

BufrContent::BufrContent(codes_handle* handle, bool delete_handle): CodesContent(handle, delete_handle) {}

BufrContent::BufrContent(const codes_handle* handle):
    BufrContent(const_cast<codes_handle*>(handle), false) {
}

BufrContent::~BufrContent() {}

eckit::message::MessageContent* BufrContent::transform(const eckit::StringDict& dict) const {
    codes_handle* h = codes_handle_clone(handle_);

    ASSERT(dict.size() <= 256);
    codes_values values[256];
    eckit::zero(values);
    size_t i = 0;
    for (auto& kv : dict) {
        // eckit::Log::info() << "kv: key " << kv.first << " value " << kv.second << std::endl;
        values[i].name         = kv.first.c_str();
        values[i].long_value   = std::stol(kv.second);
        values[i].type         = GRIB_TYPE_LONG;
        i++;
    }

    try {
        CODES_CALL(codes_set_values(h, values, i));
    }
    catch(...) {
        codes_handle_delete(h);
        throw;
    }

    return new BufrContent(h);
}


}  // namespace close
}  // namespace metkit

