// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: scan.proto

#ifndef PROTOBUF_scan_2eproto__INCLUDED
#define PROTOBUF_scan_2eproto__INCLUDED

#include <string>

#include <google/protobuf/stubs/common.h>

#if GOOGLE_PROTOBUF_VERSION < 3002000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers.  Please update
#error your headers.
#endif
#if 3002000 < GOOGLE_PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers.  Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/metadata.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include <google/protobuf/unknown_field_set.h>
// @@protoc_insertion_point(includes)
namespace proto_msg {
class LidarScan;
class LidarScanDefaultTypeInternal;
extern LidarScanDefaultTypeInternal _LidarScan_default_instance_;
}  // namespace proto_msg

namespace proto_msg {

namespace protobuf_scan_2eproto {
// Internal implementation detail -- do not call these.
struct TableStruct {
  static const ::google::protobuf::uint32 offsets[];
  static void InitDefaultsImpl();
  static void Shutdown();
};
void AddDescriptors();
void InitDefaults();
}  // namespace protobuf_scan_2eproto

// ===================================================================

class LidarScan : public ::google::protobuf::Message /* @@protoc_insertion_point(class_definition:proto_msg.LidarScan) */ {
 public:
  LidarScan();
  virtual ~LidarScan();

  LidarScan(const LidarScan& from);

  inline LidarScan& operator=(const LidarScan& from) {
    CopyFrom(from);
    return *this;
  }

  inline const ::google::protobuf::UnknownFieldSet& unknown_fields() const {
    return _internal_metadata_.unknown_fields();
  }

  inline ::google::protobuf::UnknownFieldSet* mutable_unknown_fields() {
    return _internal_metadata_.mutable_unknown_fields();
  }

  static const ::google::protobuf::Descriptor* descriptor();
  static const LidarScan& default_instance();

  static inline const LidarScan* internal_default_instance() {
    return reinterpret_cast<const LidarScan*>(
               &_LidarScan_default_instance_);
  }

  void Swap(LidarScan* other);

  // implements Message ----------------------------------------------

  inline LidarScan* New() const PROTOBUF_FINAL { return New(NULL); }

  LidarScan* New(::google::protobuf::Arena* arena) const PROTOBUF_FINAL;
  void CopyFrom(const ::google::protobuf::Message& from) PROTOBUF_FINAL;
  void MergeFrom(const ::google::protobuf::Message& from) PROTOBUF_FINAL;
  void CopyFrom(const LidarScan& from);
  void MergeFrom(const LidarScan& from);
  void Clear() PROTOBUF_FINAL;
  bool IsInitialized() const PROTOBUF_FINAL;

  size_t ByteSizeLong() const PROTOBUF_FINAL;
  bool MergePartialFromCodedStream(
      ::google::protobuf::io::CodedInputStream* input) PROTOBUF_FINAL;
  void SerializeWithCachedSizes(
      ::google::protobuf::io::CodedOutputStream* output) const PROTOBUF_FINAL;
  ::google::protobuf::uint8* InternalSerializeWithCachedSizesToArray(
      bool deterministic, ::google::protobuf::uint8* target) const PROTOBUF_FINAL;
  ::google::protobuf::uint8* SerializeWithCachedSizesToArray(::google::protobuf::uint8* output)
      const PROTOBUF_FINAL {
    return InternalSerializeWithCachedSizesToArray(
        ::google::protobuf::io::CodedOutputStream::IsDefaultSerializationDeterministic(), output);
  }
  int GetCachedSize() const PROTOBUF_FINAL { return _cached_size_; }
  private:
  void SharedCtor();
  void SharedDtor();
  void SetCachedSize(int size) const PROTOBUF_FINAL;
  void InternalSwap(LidarScan* other);
  private:
  inline ::google::protobuf::Arena* GetArenaNoVirtual() const {
    return NULL;
  }
  inline void* MaybeArenaPtr() const {
    return NULL;
  }
  public:

  ::google::protobuf::Metadata GetMetadata() const PROTOBUF_FINAL;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  // repeated bytes data = 3;
  int data_size() const;
  void clear_data();
  static const int kDataFieldNumber = 3;
  const ::std::string& data(int index) const;
  ::std::string* mutable_data(int index);
  void set_data(int index, const ::std::string& value);
  void set_data(int index, const char* value);
  void set_data(int index, const void* value, size_t size);
  ::std::string* add_data();
  void add_data(const ::std::string& value);
  void add_data(const char* value);
  void add_data(const void* value, size_t size);
  const ::google::protobuf::RepeatedPtrField< ::std::string>& data() const;
  ::google::protobuf::RepeatedPtrField< ::std::string>* mutable_data();

  // optional double timestamp = 1;
  bool has_timestamp() const;
  void clear_timestamp();
  static const int kTimestampFieldNumber = 1;
  double timestamp() const;
  void set_timestamp(double value);

  // optional uint32 seq = 2;
  bool has_seq() const;
  void clear_seq();
  static const int kSeqFieldNumber = 2;
  ::google::protobuf::uint32 seq() const;
  void set_seq(::google::protobuf::uint32 value);

  // @@protoc_insertion_point(class_scope:proto_msg.LidarScan)
 private:
  void set_has_timestamp();
  void clear_has_timestamp();
  void set_has_seq();
  void clear_has_seq();

  ::google::protobuf::internal::InternalMetadataWithArena _internal_metadata_;
  ::google::protobuf::internal::HasBits<1> _has_bits_;
  mutable int _cached_size_;
  ::google::protobuf::RepeatedPtrField< ::std::string> data_;
  double timestamp_;
  ::google::protobuf::uint32 seq_;
  friend struct  protobuf_scan_2eproto::TableStruct;
};
// ===================================================================


// ===================================================================

#if !PROTOBUF_INLINE_NOT_IN_HEADERS
// LidarScan

// optional double timestamp = 1;
inline bool LidarScan::has_timestamp() const {
  return (_has_bits_[0] & 0x00000001u) != 0;
}
inline void LidarScan::set_has_timestamp() {
  _has_bits_[0] |= 0x00000001u;
}
inline void LidarScan::clear_has_timestamp() {
  _has_bits_[0] &= ~0x00000001u;
}
inline void LidarScan::clear_timestamp() {
  timestamp_ = 0;
  clear_has_timestamp();
}
inline double LidarScan::timestamp() const {
  // @@protoc_insertion_point(field_get:proto_msg.LidarScan.timestamp)
  return timestamp_;
}
inline void LidarScan::set_timestamp(double value) {
  set_has_timestamp();
  timestamp_ = value;
  // @@protoc_insertion_point(field_set:proto_msg.LidarScan.timestamp)
}

// optional uint32 seq = 2;
inline bool LidarScan::has_seq() const {
  return (_has_bits_[0] & 0x00000002u) != 0;
}
inline void LidarScan::set_has_seq() {
  _has_bits_[0] |= 0x00000002u;
}
inline void LidarScan::clear_has_seq() {
  _has_bits_[0] &= ~0x00000002u;
}
inline void LidarScan::clear_seq() {
  seq_ = 0u;
  clear_has_seq();
}
inline ::google::protobuf::uint32 LidarScan::seq() const {
  // @@protoc_insertion_point(field_get:proto_msg.LidarScan.seq)
  return seq_;
}
inline void LidarScan::set_seq(::google::protobuf::uint32 value) {
  set_has_seq();
  seq_ = value;
  // @@protoc_insertion_point(field_set:proto_msg.LidarScan.seq)
}

// repeated bytes data = 3;
inline int LidarScan::data_size() const {
  return data_.size();
}
inline void LidarScan::clear_data() {
  data_.Clear();
}
inline const ::std::string& LidarScan::data(int index) const {
  // @@protoc_insertion_point(field_get:proto_msg.LidarScan.data)
  return data_.Get(index);
}
inline ::std::string* LidarScan::mutable_data(int index) {
  // @@protoc_insertion_point(field_mutable:proto_msg.LidarScan.data)
  return data_.Mutable(index);
}
inline void LidarScan::set_data(int index, const ::std::string& value) {
  // @@protoc_insertion_point(field_set:proto_msg.LidarScan.data)
  data_.Mutable(index)->assign(value);
}
inline void LidarScan::set_data(int index, const char* value) {
  data_.Mutable(index)->assign(value);
  // @@protoc_insertion_point(field_set_char:proto_msg.LidarScan.data)
}
inline void LidarScan::set_data(int index, const void* value, size_t size) {
  data_.Mutable(index)->assign(
    reinterpret_cast<const char*>(value), size);
  // @@protoc_insertion_point(field_set_pointer:proto_msg.LidarScan.data)
}
inline ::std::string* LidarScan::add_data() {
  // @@protoc_insertion_point(field_add_mutable:proto_msg.LidarScan.data)
  return data_.Add();
}
inline void LidarScan::add_data(const ::std::string& value) {
  data_.Add()->assign(value);
  // @@protoc_insertion_point(field_add:proto_msg.LidarScan.data)
}
inline void LidarScan::add_data(const char* value) {
  data_.Add()->assign(value);
  // @@protoc_insertion_point(field_add_char:proto_msg.LidarScan.data)
}
inline void LidarScan::add_data(const void* value, size_t size) {
  data_.Add()->assign(reinterpret_cast<const char*>(value), size);
  // @@protoc_insertion_point(field_add_pointer:proto_msg.LidarScan.data)
}
inline const ::google::protobuf::RepeatedPtrField< ::std::string>&
LidarScan::data() const {
  // @@protoc_insertion_point(field_list:proto_msg.LidarScan.data)
  return data_;
}
inline ::google::protobuf::RepeatedPtrField< ::std::string>*
LidarScan::mutable_data() {
  // @@protoc_insertion_point(field_mutable_list:proto_msg.LidarScan.data)
  return &data_;
}

#endif  // !PROTOBUF_INLINE_NOT_IN_HEADERS

// @@protoc_insertion_point(namespace_scope)


}  // namespace proto_msg

// @@protoc_insertion_point(global_scope)

#endif  // PROTOBUF_scan_2eproto__INCLUDED